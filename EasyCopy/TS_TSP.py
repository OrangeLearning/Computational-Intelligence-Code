import random
import numpy as np
import time
import copy
import math

def cmp(x):
    return x["fitness"]

def sqr(x):
    return x * x

# 点类
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Graph:
    def __init__(self,n):
        self.points = []
        self.point_n = n

    def add_point(self,p):
        self.points.append(p)
        self.point_n += 1

    def ask_distance(self,i,j):
        point_x = self.points[i]
        point_y = self.points[j]
        return math.sqrt(sqr(point_x.x - point_y.x) + sqr(point_x.y - point_y.y))

    def ask_distance_for_plan(self,plan):
        res = 0.0
        for i in range(1,self.point_n):
            res += self.ask_distance(plan[i],plan[i-1])
        res += self.ask_distance(plan[0],plan[self.point_n-1])
        # print(plan,' ',res)
        return res

    def show(self):
        for item in self.points:
            print(item.x," ",item.y)

class TS:
    def __init__(self,max_time = 40000,max_size = 100):
        self.MAX_TIME = max_time
        self.MAX_SIZE = max_size
        self.tuba_table = []

    # 初始化一个序列作为初始数据
    def initPlan(self,n):
        random.seed(time.time())
        init_plan = []
        for i in range(0,n):
            init_plan.append(i)
        
        for i in range(n):
            j = random.randint(0,n-1)
            while i == j:
                j = random.randint(0,n-1)
            init_plan[i],init_plan[j] = init_plan[j],init_plan[i]
        
        # print(init_plan)
        return init_plan

    def tuba_step(self,new_plan):
        if len(self.tuba_table) < self.MAX_SIZE:
            self.tuba_table.append(new_plan)
        else:
            sz = len(self.tuba_table)
            for i in range(1,sz):
                self.tuba_table[i-1] = self.tuba_table[i]
            self.tuba_table[sz - 1] = new_plan        

    # 从已有的一个队列中得到一个新的
    def get_new_plan(self,now_plan):
        random.seed(time.time())
        n = len(now_plan)

        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        while i == j:
            j = random.randint(0,n-1)
        
        new_plan = copy.copy(now_plan)
        # print("new_plan = ",new_plan)
        # print(i,' ',j)
        new_plan[i],new_plan[j] = new_plan[j],new_plan[i]
        return new_plan

    def get_new_plans(self,now_plan,new_cnt):
        new_plans = []
        for i in range(new_cnt):
            new_plan = self.get_new_plan(now_plan)
            while (new_plan in new_plans) or (new_plan in self.tuba_table):
                new_plan = self.get_new_plan(now_plan)
            new_plans.append(new_plan)
        return new_plans

    def run(self,n,graph):
        init_plan = self.initPlan(n)
        better_plan = {
                "fitness": graph.ask_distance_for_plan(init_plan),
                "plan": init_plan
            }
        i_time = 0
        while i_time < self.MAX_TIME:
            new_plans = self.get_new_plans(init_plan,10)
            new_res = []
            for plan in new_plans:
                _fitness = graph.ask_distance_for_plan(plan)
                new_res.append({
                    "fitness":_fitness,
                    "plan": plan
                    })

            sorted(new_res,key=cmp)
            # print(new_res,"\n")
            if new_res[0]["fitness"] < better_plan["fitness"]:
                better_plan["fitness"] = new_res[0]["fitness"]
                better_plan["plan"] = copy.copy(new_res[0]["plan"])

            # print(better_plan)
            self.tuba_step(new_res[0])
            init_plan = copy.copy(new_res[0]["plan"])

            i_time += 1
        print(better_plan)



def main():
    graph = Graph(0)
    with open("in.txt","r") as f:
        lines = f.readlines()
        for line in lines:
            line = str(line)
            # print(line)
            items = line.split(' ')
            x = float(items[1])
            y = float(items[2])
            # print('x =',x,' y = ',y)
            graph.add_point(Point(x,y))
    
    ts = TS()
    ts.run(graph.point_n,graph)
    pass

if __name__ == '__main__':
    main()
