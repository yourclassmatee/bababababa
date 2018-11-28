from flask import render_template, url_for, session, redirect, request, flash
from app import webapp
from app.timetable_db import *
import uuid
import botocore

from werkzeug.utils import secure_filename
BUCKET = 'ece1779-a3'

# event-0 for conflict
all_colors=["event-1","event-2","event-3","event-4","event-5","event-6","event-7","event-8"]

@webapp.route('/timetable/<username>')
def display_table(username):
    #if session.get('username'):
        #return redirect(url_for('dashboard', username=session.get('username')))
    #return render_template("main.html")
    photos=get_photos(username)
    photo_links=display_photo(photos)
    courses, sections=get_timetable(username)
    monday, tuesday, wednesday, thursday, friday=convert_solution(courses, sections)
    return render_template("table.html", photos=photo_links, monday_events=monday, tuesday_events=tuesday, wednesday_events=wednesday, thursday_events=thursday, friday_events=friday)


def display_photo(photos):
    s3 = boto3.client('s3')
    config = s3._client_config
    config.signature_version = botocore.UNSIGNED
    links=[]
    for file in photos:
        links.append(boto3.client('s3', config=config).generate_presigned_url('get_object', ExpiresIn=0, Params={'Bucket': BUCKET, 'Key': file}))
    return links

@webapp.route('/save_timetable', methods=['POST'])
def save_timetable():
    print("saving timetable")

    username = session.get('username')
    table_file = request.files['file']
    #print(table_file)

    photo_id = str(uuid.uuid4())

    filename = secure_filename(photo_id + '.png')
    #table_file.save(webapp.config['UPLOAD_FOLDER'] + filename + '.png')

    # try to save to s3
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    try:
        bucket.put_object(Key=filename, Body=table_file)
        object_acl = s3.ObjectAcl(BUCKET, filename)
        response = object_acl.put(ACL='public-read')

    except Exception as e:
        print(e)
        #if files are not saved then do not save to db
        print("saving to s3 fails")
    # save to dynamodb
    save_photo(username, filename)

    return "saved " + filename

def convert_solution(courses, sections):
    # courses = ["c1", "c2", "c3", "c4", "c5","c6", "c7", "c8"]
    # sections = ["M_10,M_12", "Tu_13,Tu_15", "M_12,M_14", "W_9,W_14", "Th_13,Th_15", "F_13,F_14", "M_11,M_13","M_13,M_15"]
    timetable = dict(zip(courses, sections))
    # assign colors
    course_to_color = {}
    for i in range(len(courses)):
        course_to_color[courses[i]] = all_colors[i % len(all_colors)]

    monday, tuesday, wednesday, thursday, friday = sort_by_day(timetable)

    monday_event = check_conflict(monday, course_to_color)
    tuesday_event = check_conflict(tuesday, course_to_color)
    wednesday_event = check_conflict(wednesday, course_to_color)
    thursday_event = check_conflict(thursday, course_to_color)
    friday_event = check_conflict(friday, course_to_color)
    # print(monday_event)
    # print(tuesday_event)
    # print(wednesday_event)
    # print(thursday_event)
    # print(friday_event)
    return monday_event, tuesday_event, wednesday_event, thursday_event, friday_event


def sort_by_day(sections):
    monday = {}
    tuesday = {}
    wednesday = {}
    thursday = {}
    friday = {}
    for course, time in sections.items():
        if time[0] == 'M':
            start = int(time.split(',')[0][2:])
            end = int(time.split(',')[1][2:])
            monday[course]=[start, end]
        elif time[0] == 'W':
            start = int(time.split(',')[0][2:])
            end = int(time.split(',')[1][2:])
            wednesday[course]=[start, end]
        elif time[0] == 'F':
            start = int(time.split(',')[0][2:])
            end = int(time.split(',')[1][2:])
            friday[course]=[start, end]
        elif time[1] == 'u':
            start = int(time.split(',')[0][3:])
            end = int(time.split(',')[1][3:])
            tuesday[course]=[start, end]
        elif time[1] == 'h':
            start = int(time.split(',')[0][3:])
            end = int(time.split(',')[1][3:])
            thursday[course]=[start, end]
    return monday,tuesday,wednesday,thursday,friday

def check_conflict(timetable_per_day, course_to_color):
    events=[]
    #print(timetable_per_day)
    for course_name, section in timetable_per_day.items():
        event=merge_conflict(course_name, section, timetable_per_day, course_to_color)
        events.append(event)

    overlap=[]
    for i in range(len(events)):
        for j in range (len(events)):
            if i != j and events[i][0] == 0 and events[j][0] == 0:
                start1=events[i][2][0]
                end1=events[i][2][1]
                start2 = events[i][2][0]
                end2 = events[i][2][1]
                if (start1 < start2 and start2 < end1) or (start1 < end2 and end2 < end2):
                    # conflicts still overlap
                    overlap.append([i,j])

    if len(overlap) != 0:
        print("conflict overlap detected")
    return events

def merge_conflict(course_name, section, sections, course_to_color):
    time_slots = sections.values()
    start_time = section[0]
    end_time = section[1]
    conflict = []
    start_list = []
    end_list = []
    start_list.append(start_time)
    end_list.append(end_time)
    for time in time_slots:
        test_start = time[0]
        test_end = time[1]
        if (start_time < test_start and test_start < end_time) or (start_time < test_end and test_end < end_time):
            # conflict
            conflict.append(time)
            start_list.append(test_start)
            end_list.append(test_end)
        elif (test_start < start_time and start_time < test_end) or (test_start < end_time and end_time < test_end):
            # conflict
            conflict.append(time)
            start_list.append(test_start)
            end_list.append(test_end)

    if len(conflict) != 0 :
        conflict_start = find_min(start_list)
        conflict_end = find_max(end_list)
        conflict_list = []
        for i in range(len(conflict)):
            for course, time in sections.items():
                if conflict[i] == time:
                    conflict_entry=[course, str(time[0])+":00-"+str(time[1])+":00"]
                    conflict_list.append(conflict_entry)
        # add itself
        conflict_entry = [course_name, str(start_time) + ":00-" + str(end_time) + ":00"]
        conflict_list.append(conflict_entry)
        event = [0,'event-0',[conflict_start,conflict_end],conflict_list]
        return event
    else:
        event = [1,course_to_color[course_name],[course_name,str(section[0])+":00", str(section[1])+":00"]]
        return event

def find_min(num_ist):
    min_time = 30
    for time in num_ist:
        min_time = min(time, min_time)
    return str(min_time)+":00"

def find_max(num_list):
    max_time = -1
    for time in num_list:
        max_time = max(time, max_time)
    return str(max_time)+":00"
