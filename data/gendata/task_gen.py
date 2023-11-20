import random
import csv
from datetime import datetime, timedelta
from data.gendata.com_gen import Computers
from  data.gendata.em_gen import Employees
import pandas as pd
class Task:
    def __init__(self, ID, duration: int, deadline: int, predecessor:list, computer_set:dict, skills_set: dict) -> None:
        self.ID = ID
        self.skills_set = skills_set
        self.duration = duration
        self.deadline = deadline
        self.predecessor = predecessor
        self.computer_set = computer_set
    def __str__(self) -> str:
        return "ID: {}, skills_set: {}, duration: {}, deadline: {}, predecessor: {}".format(self.ID, self.skills_set, self.duration, self.deadline, self.predecessor)
    def get_ID(self):
        return self.ID
    def get_skills_set(self):
        return self.skills_set
    def get_duration(self):
        return self.duration
    def get_deadline(self):
        return self.deadline
    def get_predecessor(self):
        return self.predecessor
    def get_computer_set(self):
        return self.computer_set
class Tasks:
    def __init__(self, ES:int, LF:int, num_tasks:int, com: Computers, em: Employees) -> None:
        self.ES = ES
        self.LF = LF
        self.num_tasks = num_tasks
        self.tasks = []
        self.com = com
        self.em = em
        self.max_duration = (LF - ES)/24
        self.max_du_task = 3
        
    def gen_tasks(self):
        
        for i in range(1, self.num_tasks+1):
            num_pre = random.randint(1,self.num_tasks//self.max_duration+1)
            
            predecessor= random.sample(range(self.num_tasks),num_pre)
            
            probability_of_one = 0.3
            random_number = random.choices([0, 1], weights=[1 - probability_of_one, probability_of_one])[0]
            if random_number == 0:
                deadline = self.LF
            else:
                # Can be changed
                deadline = self.LF - len(predecessor)*self.max_du_task - random.randint(1, self.max_duration//30)
        
            computer_set = self.at_least_com()
            skills_set = self.at_least_skill()
            task = Task(ID= i, duration = random.randint(1,self.max_du_task),deadline = deadline , predecessor= predecessor,computer_set=computer_set, skills_set=skills_set)
            self.tasks.append(task)
            
    def at_least_com(self):  
        total_coms = self.com.total_coms
        # Can be changed
        max_num_coms = total_coms//(self.num_tasks*self.max_du_task//self.max_duration+1)
        
        num_types = random.randint(1,self.com.no_type_coms//2+1)
        types = random.sample(range(1, self.com.no_type_coms+1), num_types)
        return {Type: random.randint(1,max_num_coms) for Type in types}
    
    def at_least_skill(self):
        num_type_skills = random.randint(1,self.em.no_skills//2+1 +1)
        skills_set = self.em.get_popular_skills()
        top_skills = random.choices(list(skills_set.keys()), weights=[skills_set[skill] for skill in skills_set], k=num_type_skills)
        return {skill: random.randint(1, self.em.max_level//2) for skill in top_skills}

    def save_csv(self, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['task_id', 'task_duration','task_LF','task_predecessor','task_coms_req','task_skills_req']
        
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow({
                    'task_id': task.get_ID(),
                    'task_duration': task.get_duration(),
                    # 'task_LF': task.get_deadline().strftime('%Y-%m-%d %H:%M:%S'),
                    'task_LF': task.get_deadline(),
                    'task_predecessor': task.get_predecessor(),
                    'task_coms_req': task.get_computer_set(),
                    'task_skills_req': task.get_skills_set(),
                })
            
        
        
if __name__ == "__main__":
    
    coms = Computers(10, 3, 1)
    coms_lst = coms.gen_coms()
    coms.save_csv('data/computers.csv',coms_lst)
    
    employees = Employees(12, 3, 2, 10, 1.8)
    staffs = employees.gen_employees()
    employees.save_csv('data/employees.csv',staffs)
    
    tasks = Tasks(ES = 0, LF = 720*5, num_tasks = 5, com = coms, em = employees)
    tasks.gen_tasks()
    tasks.save_csv('data/tasks.csv')
    
    print("done")
    
    