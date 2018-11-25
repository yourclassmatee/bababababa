from course_csp import *
from propagators import *
from orderings import *


testcase = [
    [[3], ["M12,M13", "W10,W11", "F18,F19"], ["Tu18,Tu19", "F10,F11", "F17,F18"], ["W9,W10", "Th13,Th14", "F14,F15"],["M12", "Tu18", "F14"]],
    [[5],["M8,M9,M10","Tu13,Tu14,Tu15"],["Tu9,Tu10","Th11,Th12","F9,F10"],["F14,F15,F16"],["M10","Tu13","W11","W14"],["Th12,Th13,Th14","F8,F9,F10"],["Tu11","Tu13","W11","F8"]],
[[8],["Th16,Th17","F9,F10","M8,M9"],["Th14,Th15,Th16","Tu10,Tu11,Tu12"],["W12,W13,W14,W15","M15,M16,M17,M18"],["M15","Th14","F12","Tu15"],["F16,F17,F18","W8,W9,W10"],["Th19,Th20","F15,F16","Th9,Th10"],["Tu9,Tu10,","Th18,Th19","M19,M20"],["Tu18,Tu19","W18,W19"],["Tu18","Tu15"]],
    #no solution case 1
    [[3],["M8,M9,M10"],["Tu8,Tu9,Tu10"],["W8,W9,W10"],["M9","Tu9","W9"]],
    #no solution case 2
    [[3],["M8,M9,M10","Th12,Th13,Th14"],["Tu8,Tu9,Tu10","Th14,Th15,Th16"],["W8,W9,W10","Th10,Th11,Th12"],["M9","Tu9","W9"]]
]

# testcase_test = [
#     #[[3],["M8,M9,M10","Th12,Th13,Th14"],["Tu8,Tu9,Tu10","Th14,Th15,Th16"],["W8,W9,W10","Th10,Th11,Th12"],["M9","Tu9","W9"]]
#     #[[3],["M12,M13","W10,W11","F18,F19"],["Tu18,Tu19","F10,F11","F17,F18"],["W9,W10","Th13,Th14","F14,F15"],["M12","Tu18","F14"]]
#     [[8],["Th16,Th17","F9,F10","M8,M9"],["Th14,Th15,Th16","Tu10,Tu11,Tu12"],["W12,W13,W14,W15","M15,M16,M17,M18"],["M15","Th14","F12","Tu15"],["F16,F17,F18","W8,W9,W10"],["Th19,Th20","F15,F16","Th9,Th10"],["Tu9,Tu10,","Th18,Th19","M19,M20"],["Tu18,Tu19","W18,W19"],["Tu18","Tu15"]]
# ]

def print_course_soln(var_array):
    for var in var_array:
        print(var.get_assigned_value())

if __name__ == "__main__":
    

    for b in testcase:
        print("Solving courses")
        csp, var_array = model_course_as_var(b)
        #csp, var_array = model_timeslot_as_var(b)
        solver = BT(csp)
        print("=======================================================")
        # print("FC")
        # solver.bt_search(prop_FC)
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_course_soln(var_array)

