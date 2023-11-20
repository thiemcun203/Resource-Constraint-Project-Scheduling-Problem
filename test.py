import csv
from ortools.sat.python import cp_model
import math
import ast  # For safely evaluating strings as Python expressions

def parse_skills(skill_str):
    try:
        return ast.literal_eval(skill_str)
    except:
        return {}

# Read data and convert to correct types
computers = []
with open('data/computers.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['quantity'] = int(row['quantity'])  # Convert quantity to integer
        row['cost'] = float(row['cost'])  # Convert cost to float
        computers.append(row)

staff = []
with open('data/employees.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['skill_set'] = parse_skills(row['skill_set'])  # Convert skill_set to dictionary
        row['salary'] = float(row['salary'])  # Convert salary to float
        staff.append(row)

tasks = []
with open('data/tasks.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        row['task_duration'] = int(row['task_duration'])  # Convert duration to integer
        row['task_predecessor'] = ast.literal_eval(row['task_predecessor'])  # Convert predecessors to list
        row['task_skills_req'] = parse_skills(row['task_skills_req'])  # Convert skill requirements to dictionary
        tasks.append(row)

# Continue with the rest of your model setup and constraint definitions

# Constants
D = 720*5  # Assuming a project duration of 720 hours for simplicity
num_computers = len(computers)
num_staff = len(staff)
num_tasks = len(tasks)

# Create the model
model = cp_model.CpModel()

# Variables
x = {}  # Task scheduling variables
y = {}  # Computer usage variables
r = {}  # Staff assignment variables
f = {}  # Number of working months for each staff
w = {}  # Wage for each staff
idle = {}  # Idle time for each staff

for t in range(num_tasks):
    for time in range(D):
        x[t, time] = model.NewBoolVar(f'x[{t},{time}]')

for t in range(num_tasks):
    for c in range(num_computers):
        y[t, c] = model.NewIntVar(0, computers[c]['quantity'], f'y[{t},{c}]')


# Constraints
# Add predecessor constraints, resource constraints, etc.
# Assuming 'task_duration' is a field in your 'tasks' that gives the duration of each task

# Create variables for start and finish times of each task
task_start = {}
task_finish = {}
for t in range(num_tasks):
    task_start[t] = model.NewIntVar(0, D, f'start_{t}')
    task_finish[t] = model.NewIntVar(0, D, f'finish_{t}')
    model.Add(task_finish[t] == task_start[t] + tasks[t]['task_duration'])
    model.Add(task_finish[t] <= int(tasks[t]['task_LF']))

# Add constraints for the predecessor tasks
for t in range(num_tasks):
    task = tasks[t]
    for p in task['task_predecessor']:
        model.Add(task_start[t] >= task_finish[p])

# Auxiliary variables for the product of y[t, c] and x[t, time]
y_x_product = {}

for t in range(num_tasks):
    for c in range(num_computers):
        for time in range(D):
            y_x_product[t, c, time] = model.NewIntVar(0, computers[c]['quantity'], f'y_x_product[{t},{c},{time}]')
            model.AddMultiplicationEquality(y_x_product[t, c, time], [y[t, c], x[t, time]])

# Add constraint for computer resource usage
for time in range(D):
    for c in range(num_computers):
        model.Add(sum(y_x_product[t, c, time] for t in range(num_tasks)) <= computers[c]['quantity'])



# Auxiliary variables for the product of r[s, t] and x[t, time]
# Correct initialization of r variables
for s in range(num_staff):
    for t in range(num_tasks):
        r[s, t] = model.NewBoolVar(f'r[{s},{t}]')

# Rest of your model setup

# Create r_x_product variables after r variables are initialized
r_x_product = {}
for s in range(num_staff):
    for t in range(num_tasks):
        for time in range(D):
            r_x_product[s, t, time] = model.NewIntVar(0, 1, f'r_x_product[{s},{t},{time}]')
            # Ensure the keys for r and x exist before creating the multiplication equality
            if (s, t) in r and (t, time) in x:
                model.AddMultiplicationEquality(r_x_product[s, t, time], [r[s, t], x[t, time]])

# Rest of your constraints and objective function


# Add constraint for staff assignment
for s in range(num_staff):
    for time in range(D):
        model.Add(sum(r_x_product[s, t, time] for t in range(num_tasks)) <= 1)


for t in range(num_tasks):
    for skill, req_level in tasks[t]['task_skills_req'].items():
        for k in range(num_staff):
            # Checking if staff k's skill level is greater or equal to the requirement
            model.Add(r[k, t] * staff[k]['skill_set'].get(skill, 0) >= r[k, t] * req_level)


for t in range(num_tasks):
    for skill, req_level in tasks[t]['task_skills_req'].items():
        model.Add(sum(r[k, t] * (staff[k]['skill_set'].get(skill, 0) >= req_level) for k in range(num_staff)) >= 1)


# Objective function
# Minimum project duration variable
min_project_duration = model.NewIntVar(0, D, 'min_project_duration')

# Set the minimum project duration as the latest task finish time
for t in range(num_tasks):
    model.Add(min_project_duration >= task_finish[t])
    
# Create a new variable for the result of min_project_duration / 720
# duration_in_months = model.NewIntVar(0, D//720+2, 'duration_in_months')
# model.AddDivisionEquality(duration_in_months, min_project_duration, 720)

# salary_factor = 100  # Factor to convert salary to an integer value

# # Convert salaries to integer values and create variables
# int_salaries = [model.NewIntVar(0, int(sal * salary_factor), f'int_salary_{s}') for s, sal in enumerate([staff_member['salary'] for staff_member in staff])]
# for s in range(num_staff):
#     model.Add(int_salaries[s] == int(staff[s]['salary'] * salary_factor))

# # Determine a reasonable upper bound for the salary per month
# min_salary = min([staff_member['salary'] for staff_member in staff]) * salary_factor
# upper_bound_salary_per_month = int(min_salary * (D // 720 + 2))

# # Adjust w[s] calculation
# for s in range(num_staff):
#     salary_per_month = model.NewIntVar(0, upper_bound_salary_per_month, f'salary_per_month_{s}')
#     model.AddMultiplicationEquality(salary_per_month, [duration_in_months, int_salaries[s]])
#     w[s] = salary_per_month

# Rest of your model setup and constraints


# Calculating total cost (wages + idle time cost)
# total_cost = model.NewIntVar(0, 1000000, 'total_cost')
# model.Add(total_cost == sum(w[s] for s in range(num_staff)))


# Combining objectives - prioritize minimizing duration, then cost, then idle time
w1, w2 = 10, 1# Example weights
combined_objective = w1*min_project_duration 
# + w2*total_cost
# Minimizing the combined objective
model.Minimize(combined_objective)


# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Output the results
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    # print(f'Total Cost: {solver.Value(total_cost)}')
    print(f'Minimize Project Duration: {solver.Value(min_project_duration)}')
    # Print other details like task scheduling, resource allocation, etc.
else:
    print('No solution found.')
