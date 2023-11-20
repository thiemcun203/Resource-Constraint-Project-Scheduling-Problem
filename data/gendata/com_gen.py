import random
import csv

import pandas as pd

def no_type_coms_func(a = 2, no_types = 5, no_coms = 100):
    deno = sum([a**(i) for i in range(no_types)])
    no_type_coms = [int(no_coms*(a**(i))/deno) for i in range(no_types-1,-1,-1)]
    no_type_coms[-1] = no_coms - sum(no_type_coms[:-1])
    return no_type_coms

def cost_func(a = 2.2, no_types = 5, base_cost = 1):
    cost = [int(base_cost*(a**(i))) for i in range(no_types)]
    return cost

class Computer:
    def __init__(self, type: int, num_coms:int ,cost_per_hour:float):
        self.type = type
        self.cost_per_hour = cost_per_hour
        self.num_coms = num_coms
    def __str__(self):
        return "type: {}, cost: {}, number of computers {}".format(self.type, self.cost_per_hour, self.num_coms)
    def get_cost(self):
        return self.cost_per_hour
    def get_type(self):
        return self.type
    def get_num_coms(self):
        return self.num_coms
class Computers:
    def __init__(self, total_coms:int, no_type_coms: int, base_cost:float):
        self.total_coms = total_coms
        self.no_type_coms = no_type_coms
        self.coms = []
        self.base_cost = base_cost
    def gen_coms(self):
        cost_lst = cost_func(no_types = self.no_type_coms, base_cost= self.base_cost)
        no_type_list = no_type_coms_func(no_types = self.no_type_coms,no_coms = self.total_coms)
        for i in range(1, self.no_type_coms+1):
            com = Computer(i, no_type_list[i-1], cost_lst[i-1])
            self.coms.append(com)
        return self.coms
    def __str__(self):
        return "number of coms: {}, no_type_coms: {}, coms: {}".format(self.num_coms, self.no_type_coms, self.coms)  
    def save_csv(self,file_path,coms):
        with open(file_path, 'w', newline = '') as csvfile:
            fieldnames = ['type','quantity','cost']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for com in coms:
                writer.writerow({
                    'type': com.get_type(),
                    'quantity':com.get_num_coms(),
                    'cost':  com.get_cost(),
                })
        
if __name__ == "__main__":
    coms = Computers(50, 5, 1)
    coms_lst = coms.gen_coms()
    coms.save_csv('data/employees.csv',coms_lst)
    df = pd.read_csv('data/employees.csv',index_col=None)
    print(df['quantity'].sum())