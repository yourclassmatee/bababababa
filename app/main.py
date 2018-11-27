
from flask import render_template, url_for, session, redirect, request, flash
from app import webapp

from app.csp_solver.course_csp import *
from app.csp_solver.propagators import *

@webapp.route('/')
def main():
    #if session.get('username'):
        #return redirect(url_for('dashboard', username=session.get('username')))
    return render_template("dashboard.html")

@webapp.route('/upload_courses', methods=['POST'])
def upload_courses():
    if(request.form):
        courses = request.form.getlist('course_id')
        print(courses)

        course_times = []
        course_times.append([len(courses)])
        for key in request.form.keys():
            if(key == "course_id"):
                continue
            sections = request.form.getlist(key)
            section_times = []
            for i in range(0,len(sections)-1, 2):
                one_section = sections[i] + "," + sections[i+1]
                #print(one_section)
                section_times.append(one_section)
            course_times.append(section_times)

        #print(course_times)
        assigned_sections = solve_course(course_times)

        return str(assigned_sections)

def solve_course(course_times):
    print("Solving courses")
    print(course_times)
    #csp, var_array = model_course_as_var([course_times])
    csp, var_array = model_course_as_var(course_times)

    solver = BT(csp)
    print("=======================================================")
    print("GAC")
    solver.bt_search(prop_GAC)
    print("Solution")
    print_course_soln(var_array)

    assigned_sections = []
    for var in var_array:
        assigned_sections.append(var.get_assigned_value())
    return assigned_sections


def print_course_soln(var_array):
    for var in var_array:
        print(var.get_assigned_value())


