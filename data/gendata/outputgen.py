import random
import csv
from datetime import datetime, timedelta

from datetime import datetime

# Define the start and end dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 4, 1)

# Calculate the time difference in seconds
time_difference_seconds = (end_date - start_date).total_seconds()

# Convert the time difference to hours
time_difference_hours = time_difference_seconds / 3600

print("Number of hours between start_date and end_date:", time_difference_hours)




# # Calculate the time range in seconds
# time_range = (end_date - start_date).total_seconds()

# # Generate a random timestamp within the range
# random_seconds = random.uniform(0, time_range)
# random_date = start_date + timedelta(seconds=random_seconds)



# tasks = [{} for i in range(10000)]
# skill_list = ["A","B","C","D"]
# com_list = ["com_X","com_Y","com_Z"]

# for i in range(10000):
#     tasks[i]["id"] = i

#     tasks[i]["start_time"] = start_date

#     tasks[i]["used_com"] = []

#     tasks[i]["staff"] = None

#     tasks[i]['total_cost'] = random.randint(400, 50000)
#     #Random resource req:

#     num_types_coms = random.choice([1,2])
#     chosen_list = []
#     for j in range(num_types_coms):

#         com_chosen = random.choice(com_list)

#         if com_chosen not in chosen_list:
#             chosen_list.append(com_chosen)
#             num_coms = random.choice([1,2,3,4])
#             tasks[i]["used_com"].append([com_chosen,num_coms])





#     #Random start time
#     random_seconds = random.uniform(0, time_range)
#     random_date = start_date + timedelta(seconds=random_seconds)



# #     tasks[i]["start_time"] = random_date
# #     random_seconds = random.uniform(0, time_range)
# #     random_date = tasks[i]["start_time"] + timedelta(seconds=random_seconds)
# #     tasks[i]["finish_time"] = random_date
# #     #RANDOM staff
# #     tasks[i]['staff_id'] = random.randint(1,100)




# for task in tasks:
#     print(task)

# with open('output.csv', 'w', newline='') as csvfile:
#     fieldnames = ['task_id', 'task_start_time', 'task_finish_time','task_com_used','staff_id','task_total_cost']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for task in tasks:
#         writer.writerow({
#             'task_id': task['id'],

#             'task_start_time': task['start_time'].strftime('%Y-%m-%d %H:%M:%S'),

#             'task_com_used': task['used_com'],
#             'staff_id': task['staff_id'],
#             'task_total_cost':task['total_cost'],
#             'task_finish_time': task['finish_time'].strftime('%Y-%m-%d %H:%M:%S')
#         })