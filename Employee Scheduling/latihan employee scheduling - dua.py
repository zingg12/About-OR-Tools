from ortools.sat.python import cp_model

#create data
num_employees = 10
num_shifts = 2
num_work_days = 5
all_employees = range(num_employees)
all_shifts = range(num_shifts)
all_work_days = range(num_work_days)

#Create the model
model = cp_model.CpModel()

#Create Shift variable
shifts = {}
for e in all_employees:
    for d in all_work_days:
        for s in all_shifts:
            shifts[(e, d,
                    s)] = model.NewBoolVar('shift_n%id%is%i' % (e, d, s))

#Assign shifts to exact one employee
for d in all_work_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(e, d, s)] for e in all_employees)

#Each employee works at most one shift per day
for e in all_employees:
    for d in all_work_days:
        model.AddAtMostOne(shifts[(e, d, s)] for s in all_shifts)

min_shifts_per_employee = (num_work_days * num_shifts) // num_employees
if num_work_days * num_shifts % num_employees == 0:
    max_shifts_per_employee = min_shifts_per_employee
else:
    max_shifts_per_employee = min_shifts_per_employee + 1
for e in all_employees:
    shifts_worked = []
    for d in all_work_days:
        for s in all_shifts:
            shifts_worked.append(shifts[(e, d, s)])
    model.Add(min_shifts_per_employee <= sum(shifts_worked))
    model.Add(sum(shifts_worked) <= max_shifts_per_employee)

solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
solver.parameters.enumerate_all_solutions = True

class EmployeesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
        def __init__(self, shifts, num_employees, num_work_days, num_shifts, limit):
            cp_model.CpSolverSolutionCallback.__init__(self)
            self._shifts = shifts
            self._num_employees = num_employees
            self._num_work_days = num_work_days
            self._num_shifts = num_shifts
            self._solution_count = 0
            self._solution_limit = limit

        def on_solution_callback(self):
            self._solution_count += 1
            print('Solution %i' % self._solution_count)
            for d in range(self._num_work_days):
                print('Day %i' % d)
                for n in range(self._num_employees):
                    is_working = False
                    for s in range(self._num_shifts):
                        if self.Value(self._shifts[(n, d, s)]):
                            is_working = True
                            print('  Employee %i works shift %i' % (n, s))
                    if not is_working:
                        print('  Employee {} does not work'.format(n))
            if self._solution_count >= self._solution_limit:
                print('Stop search after %i solutions' % self._solution_limit)
                self.StopSearch()

        def solution_count(self):
            return self._solution_count
    
solution_limit = 3
solution_printer = EmployeesPartialSolutionPrinter(shifts, num_employees,
                                                    num_work_days, num_shifts,
                                                    solution_limit)
solver.Solve(model, solution_printer)

#----------------------------------------------------------------------------
