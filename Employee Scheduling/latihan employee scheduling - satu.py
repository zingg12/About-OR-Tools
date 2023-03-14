# 1 batch magang di perusahaan pertelevisian nasional
# 1 batch terdiri dari 4 mahasiswa magang
# perusahaan tersebut menerapkan 5 hari kerja dalam seminggu yang ditetapkan secara acak
# terdapat 3 shift, yaitu pagi, siang, WFH

#import libraries
from ortools.sat.python import cp_model
import random

#Crate data 
num_interns = 4
num_shifts = 3
num_days = 5
all_interns = range(num_interns)
all_shifts = range(num_shifts)
# all_days = range(num_days)

#create list possible work days for a week
work_days = []

#shuffle list of work days randomly
random.shuffle(work_days)

#select 5 first wprk days from the shuffled list
selected_days = work_days[:num_days]

#create model
model = cp_model.CpModel()

#Create shift variable
shifts = {}
for i in all_interns: 
    for d in selected_days:
        for s in all_shifts:
            shifts[(i, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (i, d, s))

#Assign shift to exactly one internship
for d in selected_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(i, d, s)] for i in all_interns)

#Internship works at most one shift per day
for n in all_interns:
    for d in selected_days:
        model.AddAtMostOne(shifts[(i, d, s)] for s in all_shifts)

min_shifts_per_interns = (num_shifts * num_days) // num_interns
if num_shifts * num_days % num_interns == 0: 
    max_shifts_per_interns = min_shifts_per_interns
else:
    max_shifts_per_interns = min_shifts_per_interns + 1
for i in all_interns:
    shifts_worked = []
    for d in selected_days:
        for s in all_shifts:
            shifts_worked.append(shifts[(i, d, s)])
    model.Add(min_shifts_per_interns <= sum(shifts_worked))
    model.Add(sum(shifts_worked) <= max_shifts_per_interns)

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True


#-----------DARI AI--------------
# import random
# from ortools.sat.python import cp_model

# # Define the number of employees, shifts, and work days
# num_employees = 4
# num_shifts = 3
# num_work_days = 5

# # Define the shift durations
# shift_durations = [8, 8, 8]  # 8 hours per shift

# # Create a list of all possible work days for the week
# work_days = [...]  # List of dates for the week

# # Shuffle the list of work days randomly
# random.shuffle(work_days)

# # Select the first five work days from the shuffled list
# selected_days = work_days[:num_work_days]

# # Create a CP-SAT model
# model = cp_model.CpModel()

# # Define the decision variables
# shifts = {}  # Dictionary of (employee, day, shift) -> boolean variable

# for employee in range(num_employees):
#     for day in selected_days:
#         for shift in range(num_shifts):
#             var_name = f"shift_{employee}_{day}_{shift}"
#             shifts[(employee, day, shift)] = model.NewBoolVar(var_name)

# # Add the constraints
# for day in selected_days:
#     for shift in range(num_shifts):
#         # Constraint 1: Each shift must be assigned to exactly one employee
#         shift_vars = [shifts[(employee, day, shift)] for employee in range(num_employees)]
#         model.Add(sum(shift_vars) == 1)

#     for employee in range(num_employees):
#         # Constraint 2: Each employee must be assigned to exactly one shift per day
#         employee_vars = [shifts[(employee, day, shift)] for shift in range(num_shifts)]
#         model.Add(sum(employee_vars) == 1)

# # Add the objective function
# objective = sum(shifts.values())
# model.Maximize(objective)

# # Solve the optimization problem
# solver = cp_model.CpSolver()
# status = solver.Solve(model)

# # Get the optimized schedule
# schedule = {}

# for employee in range(num_employees):
#     for day in selected_days:
#         for shift in range(num_shifts):
#             if solver.Value(shifts[(employee, day, shift)]) == 1:
#                 schedule[(employee, day)] = shift

# # Print the schedule
# for employee in range(num_employees):
#     print(f"Employee {employee}:")
#     for day in selected_days:
#         shift = schedule[(employee, day)]
#         print(f"  {day}: Shift {shift} ({shift_durations[shift]} hours)")

