#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 00:18:53 2018

@author: orangeluyao

Particle Swarm Optimization
"""

import copy
import random
import math
import time



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

class Node:
    def __init__(self,plan,fitness):
        self.fitness = fitness
        self.plan = copy.copy(plan)
        self.best = fitness


class PSO:
    def __init__(self,max_group = 100,max_time=1000):
        self.MAX_TIME = max_time
        self.MAX_GROUP = max_group
        pass

    def init_plan(self,n):
        random.seed(time.time())
        init_plan = []
        for i in range(0, n):
            init_plan.append(i)

        for i in range(n):
            j = random.randint(0, n - 1)
            while i == j:
                j = random.randint(0, n - 1)
            init_plan[i], init_plan[j] = init_plan[j], init_plan[i]

        return init_plan


    def init_group(self,n,graph):
        group = []
        for i in range(self.MAX_GROUP):
            new_plan = self.init_plan(n)
            new_fitness = graph.ask_distance_for_plan(new_plan)

            while Node(new_plan,new_fitness) in group:
                new_plan = self.init_plan(n)
                new_fitness = graph.ask_distance_for_plan(new_plan)

            group.append(Node(new_plan,new_fitness))
        return group

    def run(self,n,graph):
        random.seed(time.time())
        group = self.init_group(n,graph)
        
        i_time = 0
        while i_time < self.MAX_TIME:
            
            
            i_time += 1


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

    pso = PSO()
    pso.run(graph.point_n,graph)

if __name__ == '__main__':
    main()
