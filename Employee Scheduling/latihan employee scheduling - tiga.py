from ortools.sat.python import cp_model

num_interns = 5
num_work_days = 5
num_shifts = 3 # 0 -> pagi, 1 -> siang, 2 -> WFH
all_num_interns = range(num_interns)
all_num_work_days = range(num_work_days)
all_num_shifts = range(num_shifts)

model = cp_model.CpModel()

#Create Shift Variable
shifts = {}
for i in all_num_interns:
    for d in all_num_work_days:
        for s in all_num_shifts:
            shifts[(i, d, s)] = model.NewBoolVar('shift_i%id%is%i' % (i, d, s))

#Add Constraints
for d in all_num_work_days:
    for s in all_num_shifts:
        model.AddExactlyOne(shifts[(i, d, s)] for i in all_num_interns)

for i in all_num_interns:
    for d in all_num_work_days:
        model.AddAtMostOne(shifts[(i, d, s)] for s in all_num_shifts)

min_shifts_per_interns = (num_work_days * num_shifts) // num_interns
if num_work_days * num_shifts % num_interns == 0:
    max_shifts_per_interns = min_shifts_per_interns
else:
    