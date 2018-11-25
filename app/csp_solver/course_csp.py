#Look for #IMPLEMENT tags in this file.

'''
Construct and return Kenken CSP model.
'''

from cspbase import *
import itertools

def model_course_as_var(course_list):

    course_num = course_list[0][0]
    # list of timeslots e.g.["M10","Tu10","W16"]
    no_go = course_list[course_num + 1]
    # generate vars
    vars = []
    for i in range(1, course_num+1):
        vars.append(Variable('V{}'.format(i), course_list[i]))

    cons = []

    # add all diff constraint for each course
    for i in range(0, len(vars)):
        sat_tuples = []
        for j in range(i+1, len(vars)):
            sat_tuples = check_vars(vars[i].domain(), vars[j].domain())

            con = Constraint("C(CS{},CS{})".format(i + 1, j + 1), [vars[i], vars[j]])
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)


    #add constraints for nogo times
    for i in range(0, len(vars)):
        sat_tuples = []

        for session in vars[i].domain():
            session_ok = True
            for nogo_time in no_go:
                if nogo_time in session:
                    session_ok = False
                    break
            if session_ok == True:
                sat_tuples.append((session,))


        con = Constraint("C(CS{},nogo)".format(i + 1,), [vars[i]])
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    #make csp
    course_csp = CSP("course_csp")

    # add all vars
    for var in vars:
        course_csp.add_var(var)

    # add all constraints
    for each_con in cons:
        course_csp.add_constraint(each_con)

    #print ("finish")
    return course_csp, vars


def model_timeslot_as_var(course_list):

    course_num = course_list[0][0]

    var_array = []
    var_dict = dict()

    domain = ["CS1", "CS2", "CS3", "CS4", "CS5", "Empty"]

    #make vars for each session hour
    for i in range (0, course_num):
        course = course_list[i+1]
        for session in course:
            session_hours = session.split(',')

            for hour in session_hours:
                if hour not in var_dict:
                    #var name, domain
                    new_var = Variable(hour, domain)
                    var_array.append(new_var)
                    var_dict[hour] = new_var

    #sort by var name
    var_array.sort(key = lambda variable : variable.name )

    print("made vars")

    #make constraints for each session so that each session is complete
    cons = []

    for i in range (0, course_num):
        course = course_list[i+1]

        for j in range(0, len(course)):
            session = course[j]
            scope = []
            session_hours = session.split(',')

            for hour in session_hours:
                scope.append(var_dict[hour])

            con = Constraint("C(CS{},SN{})".format(i + 1, j + 1), scope)

            #make sat_tuples based on num of hours in session
            sat_tuples = []

            val_list = []
            empty_list =[]

            for k in range(0,len(session_hours)):
                val_list.append("CS" + str(i+1))
                empty_list.append("Empty")

            if len(val_list) == 1:
                #make sure we append a tuple
                sat_tuples.append((val_list[0],))
                sat_tuples.append((empty_list[0],))
            else:
                sat_tuples.append(tuple(val_list))
                sat_tuples.append(tuple(empty_list))

            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

    print("made cons")

    #make csp
    course_csp = CSP("course_csp")

    # add all vars
    for var in var_array:
        course_csp.add_var(var)

    # add all constraints
    for each_con in cons:
        course_csp.add_constraint(each_con)

    #print ("finish")
    return course_csp, var_array

def check_vars(d0, d1):
    sat_tuples = []

    for t in itertools.product(d0, d1):
        #if (t[1] not in t[0]) and (t[0] not in t[1]):
            #sat_tuples.append(t)
        invalid = False
        time_list = t[0].strip().split(",")
        for time_slot in time_list:
            if time_slot in t[1]:
                invalid = True
        if not invalid:
            sat_tuples.append(t)

    return sat_tuples




