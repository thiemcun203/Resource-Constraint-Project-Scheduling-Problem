from collections import Counter
import random
import csv
import statistics

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class Employee:
    def __init__(self, ID, skills_set: dict, base_cost:float, s) -> None:
        self.ID = ID
        self.skills_set = skills_set
        self.base_cost = base_cost
        self.s = s
    def __str__(self) -> str:
        return "ID: {}, skills_set: {}, cost: {}".format(self.ID, self.skills_set, self.cost)
    def get_ID(self):
        return self.ID
    def get_skills_set(self):
        return self.skills_set
    def get_cost(self):
        return self.cost
    def get_level(self):
        return sum([self.s**self.skills_set[skill] for skill in self.skills_set])
    def get_cost(self):
        return self.base_cost*self.get_level()


class Employees:
    def __init__(self, total_employees:int, no_skills: int, max_level :int, base_cost:float, s) -> None:
        self.total_employees = total_employees
        self.no_skills = no_skills
        self.employees = []
        self.max_level = max_level
        self.base_cost = base_cost
        self.s = s
        assert self.max_level <= 10
        assert self.no_skills <= 10
    def get_maximal_possible_value_level(self) -> list:
        from itertools import product

        def generate_numbers(k, n):
        # Generate all possible combinations of digits from 1 to k with repetition
            digit_combinations = list(product(range(1, k + 1), repeat=n))

            # Convert each combination to a sorted list to make order-independent
            sorted_combinations = [sorted(combination) for combination in digit_combinations]

            # Remove duplicates by converting to a set and then back to a list
            result = list(map(list, set(map(tuple, sorted_combinations))))

            return result
        
        X = []
        
        for s in range(1,self.no_skills+1):
            for l in range(1,self.max_level+1):
                for poss in generate_numbers(l,s):
                    em = [value for value in poss]
                    X.append((em, sum([self.s**value for value in em]) ))
        sorted_list = sorted(X, key=lambda x: x[1])            
                    
        return sorted_list
    def generate_distribution(self, plot = False):
        X = self.get_maximal_possible_value_level()
        X_values = [item[1] for item in X]

        mu, std = norm.fit(X_values)
        num_samples = self.total_employees
        
        prob = norm.pdf(X_values, mu, std)
        total_probability = sum(prob)
        probabilities = [p / total_probability for p in prob]
        
        indices = np.arange(len(X_values))
        random_index_sample = np.random.choice(indices, size=num_samples, p=probabilities)
    
    
        final_sample = [X[index] for index in random_index_sample]
        if plot: 
            random_sample = sorted([(X_values[index],index) for index in random_index_sample])
            random_sample_prob = [prob[item[1]] for item in random_sample]
            # Plot the line
            plt.plot(X_values,prob, marker='o', linestyle='-', color='b', label='Total Possible')
            # Add labels and title
            plt.xlabel('Level')
            plt.ylabel('Probability having this level')
            plt.hist([item[0] for item in random_sample], density=True, alpha=0.6, color='g')
            plt.plot([item[0] for item in random_sample],random_sample_prob, marker='o', linestyle='-', color='r', label='Sample')
            # Add a legend
            plt.legend()
            # Show the plot
            output_directory = 'data'  # Replace with your desired directory path
            output_filename = 'employees_plot.png'          # Replace with your desired filename
            output_path = f'{output_directory}/{output_filename}'

            plt.savefig(output_path)
            # plt.show()
        
        return final_sample
    def gen_employees(self):
        for i, item in zip(range(1,self.total_employees+1), self.generate_distribution(plot = True)):
            skills = random.sample(range(1,self.no_skills+1), len(item[0]))
            skills_set = dict(zip(skills,item[0]))
            em = Employee(i, skills_set, self.base_cost, self.s)
            self.employees.append(em)
        return self.employees
    
    def get_popular_skills(self):
        skills = [list(em.get_skills_set().keys()) for em in self.employees]
        skills_set = [item for sublist in skills for item in sublist]
        skills_dict = Counter(skills_set)
        S = sum([value for value in skills_dict.values()])
        skills_set = {skill: value/S for skill,value in skills_dict.items()}
        return skills_set
    
    def save_csv(self, file_path, staffs):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['id','skill_set','salary']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for staff in staffs:
                writer.writerow({
                    'id': staff.get_ID(),
                    'skill_set':staff.get_skills_set(),
                    'salary':  int(staff.get_cost()),
                })
        
if __name__ == "__main__":
    employees = Employees(100, 6, 5, 100, 1.8)
    staffs = employees.gen_employees()
    
    
    

# with open('tasks.csv', 'w', newline='') as csvfile:
#     fieldnames = ['task_id', 'task_skill_requirement', 'task_ES', 'task_LF','task_predecessor','task_duration','task_com_req','task_cloud_req']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for task in tasks:
#         writer.writerow({
#             'task_id': task['id'],
#             'task_skill_requirement': ', '.join(task['req_skill']),
#             'task_ES': task['ES'].strftime('%Y-%m-%d %H:%M:%S') if random.random() <= 0.7 else '',
#             'task_LF': task['LF'].strftime('%Y-%m-%d %H:%M:%S')if random.random() <= 0.7 else '' ,
#             'task_predecessor': task['predecessor'],
#             'task_duration': task['duration'],
#             'task_com_req': task['req_com'],
#             'task_cloud_req': task['cloud_unit']
#         })
        
        
    