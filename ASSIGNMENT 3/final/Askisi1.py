import pandas as pd
import csp
import random
import time

# LOAD THE EXAM DATA FROM THE CSV FILE
data = pd.read_csv('h3-data.csv')

# DEFINE THE AVAILABLE DAYS AND PERIODS
DAYS = list(range(1, 22))  # 21 DAYS
PERIODS = ['9-12', '12-3', '3-6']  # THREE TIME PERIODS EACH DAY
TIME_SLOTS = [(day, period) for day in DAYS for period in PERIODS]

# EXTRACT THE LIST OF EXAMS FROM THE DATA
EXAMS = data['Μάθημα'].tolist()

# DEFINE THE DOMAINS FOR EACH EXAM AS ALL POSSIBLE TIME SLOTS
DOMAINS = {exam: TIME_SLOTS.copy() for exam in EXAMS}

# INITIALIZE CONSTRAINT WEIGHTS
constraint_weights = {}

# DEFINE THE CONSTRAINTS BETWEEN TWO EXAMS
def constraints(exam1, slot1, exam2, slot2):
    day1, period1 = slot1
    day2, period2 = slot2

    global constraint_weights
    exam_csp.constraints_checked += 1  # INCREMENT CONSTRAINTS CHECKED

    if slot1 == slot2:
        # SAME SLOT CONSTRAINT: EXAMS CANNOT BE SCHEDULED IN THE SAME TIME SLOT
        key = tuple(sorted((exam1, exam2)))
        constraint_weights[key] = constraint_weights.get(key, 1) + 1
        return False  # CONSTRAINT VIOLATION

    semester1 = data[data['Μάθημα'] == exam1]['HΕξάμηνο'].values[0]
    semester2 = data[data['Μάθημα'] == exam2]['HΕξάμηνο'].values[0]
    if semester1 == semester2 and day1 == day2:
        # SAME SEMESTER SAME DAY CONSTRAINT: EXAMS FROM THE SAME SEMESTER CANNOT BE ON THE SAME DAY
        key = tuple(sorted((exam1, exam2)))
        constraint_weights[key] = constraint_weights.get(key, 1) + 1
        return False  # CONSTRAINT VIOLATION

    prof1 = data[data['Μάθημα'] == exam1]['Καθηγητής'].values[0]
    prof2 = data[data['Μάθημα'] == exam2]['Καθηγητής'].values[0]
    if prof1 == prof2 and day1 == day2:
        # SAME PROFESSOR SAME DAY CONSTRAINT: EXAMS WITH THE SAME PROFESSOR CANNOT BE ON THE SAME DAY
        key = tuple(sorted((exam1, exam2)))
        constraint_weights[key] = constraint_weights.get(key, 1) + 1
        return False  # CONSTRAINT VIOLATION

    difficult1 = data[data['Μάθημα'] == exam1]['Δύσκολο (TRUE/FALSE)'].values[0]
    difficult2 = data[data['Μάθημα'] == exam2]['Δύσκολο (TRUE/FALSE)'].values[0]
    if difficult1 == 'TRUE' and difficult2 == 'TRUE':
        if abs(day1 - day2) < 2:
            # DIFFICULT EXAMS PROXIMITY CONSTRAINT: HARD EXAMS MUST BE AT LEAST 2 DAYS APART
            key = tuple(sorted((exam1, exam2)))
            constraint_weights[key] = constraint_weights.get(key, 1) + 1
            return False  # CONSTRAINT VIOLATION

    has_lab1 = data[data['Μάθημα'] == exam1]['Εργαστήριο (TRUE/FALSE)'].values[0]
    has_lab2 = data[data['Μάθημα'] == exam2]['Εργαστήριο (TRUE/FALSE)'].values[0]
    if has_lab1 == 'TRUE' and exam2.startswith(exam1):
        PERIODS_ORDER = ['9-12', '12-3', '3-6']
        try:
            next_period = PERIODS_ORDER[PERIODS_ORDER.index(period1) + 1]
            if not (day1 == day2 and period2 == next_period):
                # LAB FOLLOW-UP CONSTRAINT: LAB EXAM MUST FOLLOW IMMEDIATELY AFTER THE THEORY EXAM
                key = tuple(sorted((exam1, exam2)))
                constraint_weights[key] = constraint_weights.get(key, 1) + 1
                return False  # CONSTRAINT VIOLATION
        except IndexError:
            key = tuple(sorted((exam1, exam2)))
            constraint_weights[key] = constraint_weights.get(key, 1) + 1
            return False  # CONSTRAINT VIOLATION
    if has_lab2 == 'TRUE' and exam1.startswith(exam2):
        PERIODS_ORDER = ['9-12', '12-3', '3-6']
        try:
            next_period = PERIODS_ORDER[PERIODS_ORDER.index(period2) + 1]
            if not (day1 == day2 and period1 == next_period):
                # LAB FOLLOW-UP CONSTRAINT: LAB EXAM MUST FOLLOW IMMEDIATELY AFTER THE THEORY EXAM
                key = tuple(sorted((exam1, exam2)))
                constraint_weights[key] = constraint_weights.get(key, 1) + 1
                return False  # CONSTRAINT VIOLATION
        except IndexError:
            key = tuple(sorted((exam1, exam2)))
            constraint_weights[key] = constraint_weights.get(key, 1) + 1
            return False  # CONSTRAINT VIOLATION

    return True  # NO CONSTRAINT VIOLATION

# CREATE THE NEIGHBORS DICTIONARY FOR EACH EXAM
NEIGHBORS = {exam: [e for e in EXAMS if e != exam] for exam in EXAMS}

# INITIALIZE THE CSP WITH VARIABLES, DOMAINS, NEIGHBORS, AND CONSTRAINTS
exam_csp = csp.CSP(
    variables=EXAMS,
    domains=DOMAINS,
    neighbors=NEIGHBORS,
    constraints=constraints
)

# INITIALIZE METRICS
exam_csp.nassigns = 0
exam_csp.constraints_checked = 0

# DEFINE THE DOM/WDEG HEURISTIC BASED ON THE PAPER
def dom_wdeg(assignment, csp_instance):
    unassigned = [v for v in csp_instance.variables if v not in assignment]
    if not unassigned:
        return None

    def weighted_degree(var):
        # SUM THE WEIGHTS OF ALL CONSTRAINTS INVOLVING VAR
        total_weight = 0
        for neighbor in csp_instance.neighbors[var]:
            key = tuple(sorted((var, neighbor)))
            total_weight += constraint_weights.get(key, 1)  # DEFAULT WEIGHT IS 1
        return total_weight

    # SELECT VARIABLE WITH MINIMUM DOMAIN SIZE / WEIGHTED DEGREE
    return min(
        unassigned,
        key=lambda var: len(csp_instance.domains[var]) / weighted_degree(var) if weighted_degree(var) > 0 else float('inf')
    )

# SOLVE USING MRV HEURISTIC WITH FORWARD CHECKING
print("\nSOLVING WITH MRV HEURISTIC AND FORWARD CHECKING:")
print("-----------------------------------------------")

start_time = time.time()
solution_fc_mrv = csp.backtracking_search(
    exam_csp,
    select_unassigned_variable=csp.mrv,
    inference=csp.forward_checking 
)
end_time = time.time()
print("SOLUTION WITH MRV AND FORWARD CHECKING:")
print(solution_fc_mrv)
print(f"Time: {end_time - start_time} Assigns: {exam_csp.nassigns} Constrains: {exam_csp.constraints_checked}")

# RESET METRICS BEFORE NEXT SOLUTION
exam_csp.nassigns = 0
exam_csp.constraints_checked = 0

# SOLVE USING MRV HEURISTIC WITH MAC
print("\nSOLVING WITH MRV HEURISTIC AND MAC:")
print("------------------------------------")

start_time = time.time()
solution_mac_mrv = csp.backtracking_search(
    exam_csp,
    select_unassigned_variable=csp.mrv,
    inference=csp.mac
)
end_time = time.time()
print("SOLUTION WITH MRV AND MAC:")
print(solution_mac_mrv)
print(f"Time: {end_time - start_time} Assigns: {exam_csp.nassigns} Constrains: {exam_csp.constraints_checked}")

# RESET METRICS BEFORE NEXT SOLUTION
exam_csp.nassigns = 0
exam_csp.constraints_checked = 0

# SOLVE USING DOM/WDEG HEURISTIC WITH FORWARD CHECKING
print("\nSOLVING WITH DOM/WDEG HEURISTIC AND FORWARD CHECKING:")
print("-----------------------------------------------------")

start_time = time.time()
solution_fc_domwdeg = csp.backtracking_search(
    exam_csp,
    select_unassigned_variable=dom_wdeg,
    inference=csp.forward_checking 
)
end_time = time.time()
print("SOLUTION WITH DOM/WDEG AND FORWARD CHECKING:")
print(solution_fc_domwdeg)
print(f"Time: {end_time - start_time} Assigns: {exam_csp.nassigns} Constrains: {exam_csp.constraints_checked}")

# RESET METRICS BEFORE NEXT SOLUTION
exam_csp.nassigns = 0
exam_csp.constraints_checked = 0

# SOLVE USING DOM/WDEG HEURISTIC WITH MAC
print("\nSOLVING WITH DOM/WDEG HEURISTIC AND MAC:")
print("----------------------------------------")

start_time = time.time()
solution_mac_domwdeg = csp.backtracking_search(
    exam_csp,
    select_unassigned_variable=dom_wdeg,
    inference=csp.mac
)
end_time = time.time()
print("SOLUTION WITH DOM/WDEG AND MAC:")
print(solution_mac_domwdeg)
print(f"Time: {end_time - start_time} Assigns: {exam_csp.nassigns} Constrains: {exam_csp.constraints_checked}")

# RESET METRICS BEFORE NEXT SOLUTION
exam_csp.nassigns = 0
exam_csp.constraints_checked = 0

# SOLVE USING MIN-CONFLICTS (DOESN'T USE VARIABLE ORDERING HEURISTIC)
print("\nSOLVING WITH MIN-CONFLICTS:")
print("-----------------------------")

start_time = time.time()
solution_min_conflicts = csp.min_conflicts(
    exam_csp,
    max_steps=1000
)
end_time = time.time()
print("SOLUTION WITH MIN-CONFLICTS:")
print(solution_min_conflicts)
print(f"Time: {end_time - start_time} Assigns: {exam_csp.nassigns} Constrains: {exam_csp.constraints_checked}")