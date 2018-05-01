#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 02:11:26 2018

@author: orangeluyao

simulated annealing

"""
import copy
import math
import random
import time
from queue import Queue

def sqr(x):
    return x * x

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

class SA:
    def __init__(self,t_max,t_min,L,q):
        self.T_MAX = t_max
        self.T_MIN = t_min
        self.L = L
        self.q = q
        
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
            
        return init_plan
    
    def get_new_plan(self,now_plan):
        random.seed(time.time())
        n = len(now_plan)

        i = random.randint(0,n-1)
        j = random.randint(0,n-1)
        while i == j:
            j = random.randint(0,n-1)
        
        new_plan = copy.copy(now_plan)
        new_plan[i],new_plan[j] = new_plan[j],new_plan[i]
        return new_plan
    
    def run(self,n,graph):
        random.seed(time.time())
        init_plan = self.initPlan(n)
        T = self.T_MAX
        
        res = {
                "fitness": graph.ask_distance_for_plan(init_plan),
                "plan": init_plan
                }
        
        count = 0
        
        while T > self.T_MIN:
            for i in range(self.L):
                new_plan = copy.copy(init_plan)
                new_plan = self.get_new_plan(new_plan)
                count += 1
                
                init_fitness = graph.ask_distance_for_plan(init_plan)
                new_fitness  = graph.ask_distance_for_plan(new_plan)
            
                if res["fitness"] > init_fitness:
                    res["fitness"] = init_fitness
                    res["plan"] = copy.copy(init_plan)
                if res["fitness"] > new_fitness:
                    res["fitness"] = new_fitness
                    res["plan"] = new_plan
                
                # print("fitness = ",init_fitness," plan :\n",init_plan)                
                delta_fitness = new_fitness - init_fitness
                # print("delta = ",delta_fitness)
                # if the fitness get smaller , then it should be good
                # if the fitness get bigger , the it can be accepted by rate
                if delta_fitness >= 0:
                    div = random.random()
                    metropolis = math.exp(-delta_fitness / T)
                    
                    if metropolis <= div:
                        init_plan = copy.copy(new_plan)
                else:
                    init_plan = copy.copy(new_plan)
            T *= self.q
            
        print(res)
        

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
    
    sa = SA(100000,10,50,0.98)
    sa.run(graph.point_n,graph)
    
    pass
if __name__ == '__main__':
    main()