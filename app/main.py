
from flask import render_template, url_for, session, redirect, request, flash
from app import webapp
from app.login import check_session

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
        form_list = request.form.getlist('courses')

        #form_list = ['EFWEFEWF', 'M', '9', '10', 'Tu', '9', '11', '', 'GIRGURG', 'Tu', '10', '11', '']
        print(form_list)

        courses = []

        course_times = []

        i=0
        while i < len(form_list):
            if len(form_list[i]) > 2:
                courses.append(form_list[i])
                #print(courses)
                i += 1
            else:
                j = i
                sections_one_course = []
                while form_list[j] != "":
                    #make single section
                    start = form_list[j] + "_" + form_list[j+1]
                    end = form_list[j] + "_" + form_list[j+2]
                    single_section = start + "," + end
                    sections_one_course.append(single_section)
                    #print(sections_one_course)
                    j+=3

                course_times.append(sections_one_course)
                #print(course_times)
                i = j+2


        #add num of courses
        course_times.insert(0, [len(course_times)])

        print(course_times)
        assigned_sections = solve_course(course_times)

        return str(assigned_sections)

def solve_course(course_times):

    #course_times = [[3], ["M_12,M_13", "W_10,W_11", "F_18,F_19"], ["M_11,M_14", "F_10,F_11", "F_17,F_18"], ["W_9,W_10", "Th_13,Th_14", "F_14,F_15"]]
    #course_times = [[3],["Tu_8,Tu_10"],["M_8,M_10"],["M_8,M_10"]]

    print("Solving courses")
    #print(course_times)
    #csp, var_array = model_course_as_var([course_times])
    csp, var_array = model_course_as_var(course_times)

    solver = BT(csp)
    solver.bt_search(prop_GAC)
    print_course_soln(var_array)

    assigned_sections = []
    for var in var_array:
        assigned_sections.append(var.get_assigned_value())


    # 1 conflict


    if None in assigned_sections:
        course_times_mod = course_times.copy()
        course_times_mod[0][0] -= 1
        print("1 conflict")
        removing = 1
        while None in assigned_sections and removing <= len(course_times):


            course_times_mod.pop(removing)
            #print("removing %d"%removing)
            #print("running alog with")
            #print(course_times_mod)
            csp, var_array = model_course_as_var(course_times_mod)
            solver = BT(csp)
            solver.bt_search(prop_GAC)
            assigned_sections = []
            for var in var_array:
                assigned_sections.append(var.get_assigned_value())
            if None not in assigned_sections:
                #add back 0th section from removed course
                assigned_sections.insert(removing-1, course_times[removing][0])
            removing += 1
            course_times_mod = course_times.copy()

    return assigned_sections


def print_course_soln(var_array):
    for var in var_array:
        print(var.get_assigned_value())


@webapp.route('/dashboard/<username>')
def dashboard(username):

    if(check_session(username)):

        return render_template('dashboard.html')
    else:
        flash("Error: you are not logged in")
        return redirect(url_for('login'))

