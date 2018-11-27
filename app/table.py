from flask import render_template, url_for, session, redirect, request, flash
from app import webapp


@webapp.route('/timetable')
def display_table():
    #if session.get('username'):
        #return redirect(url_for('dashboard', username=session.get('username')))
    #return render_template("main.html")
    monday = {'event-5':[0,["10:00","12:00"],[["circuit","10:00-12:00"],["math","11:00-12:00"]]],
              'event-1':[1,["circuit", "13:00", "15:00"]]
              }
    course=["c1", "c2", "c3"]
    section=["M10,M11", "Tu", "Th", "F", "W"]
    return render_template("table.html", monday_events=monday)

@webapp.route('/save_timetable', methods=['POST'])
def save_timetable():
    print("saving timetable")

    table_file = request.files['file']
    print(table_file)

    table_file.save(webapp.config['UPLOAD_FOLDER'] + table_file.filename + '.png')


    return ""