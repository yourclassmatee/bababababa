from flask import render_template, url_for, session, redirect, request, flash
from app import webapp

# event-0 for conflict
all_colors=["event-1","event-2","event-3","event-4","event-5","event-6","event-6","event-7","event-8"]

@webapp.route('/timetable')
def display_table():
    #if session.get('username'):
        #return redirect(url_for('dashboard', username=session.get('username')))
    #return render_template("main.html")
    monday, tuesday, wednesday, thursday, friday=convert_solution()
    return render_template("table.html", monday_events=monday, tuesday_events=tuesday, wednesday_events=wednesday, thursday_events=thursday, friday_events=friday)

@webapp.route('/save_timetable', methods=['POST'])
def save_timetable():
    print("saving timetable")

    table_file = request.files['file']
    print(table_file)

    table_file.save(webapp.config['UPLOAD_FOLDER'] + table_file.filename + '.png')


    return ""

def convert_solution():
    courses = ["c1", "c2", "c3", "c4", "c5","c6", "c7", "c8"]
    #section = ["M10,M11", "Tu", "Th", "F", "W"]
    sections = ["M10,M12", "Tu13,Tu15", "M12,M14", "W9,W14", "Th13,Th15", "F13,F14", "M11,M13","M13,M15"]
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
    print(monday_event)
    print(tuesday_event)
    print(wednesday_event)
    print(thursday_event)
    print(friday_event)
    return monday_event, tuesday_event, wednesday_event, thursday_event, friday_event


def sort_by_day(sections):
    monday = {}
    tuesday = {}
    wednesday = {}
    thursday = {}
    friday = {}
    for course, time in sections.items():
        if time[0] == 'M':
            start = int(time.split(',')[0][1:])
            end = int(time.split(',')[1][1:])
            monday[course]=[start, end]
        elif time[0] == 'W':
            start = int(time.split(',')[0][1:])
            end = int(time.split(',')[1][1:])
            wednesday[course]=[start, end]
        elif time[0] == 'F':
            start = int(time.split(',')[0][1:])
            end = int(time.split(',')[1][1:])
            friday[course]=[start, end]
        elif time[1] == 'u':
            start = int(time.split(',')[0][2:])
            end = int(time.split(',')[1][2:])
            tuesday[course]=[start, end]
        elif time[1] == 'h':
            start = int(time.split(',')[0][2:])
            end = int(time.split(',')[1][2:])
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
