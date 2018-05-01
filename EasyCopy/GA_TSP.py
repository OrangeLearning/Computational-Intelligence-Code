#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 1 02:11:26 2018

@author: orangeluyao

Genetic Algorithm

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

class GA:
    def __init__(self,max_time,max_group,mute_rate):
        self.MAX_TIME = max_time
        self.MAX_GROUP = max_group
        self.MUTE_RATE = mute_rate
        
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
    
    def init_group(self,n):
        groups = []
        for i in range(self.MAX_GROUP):
            plan = self.initPlan(n)
            while plan in groups:
                plan = self.initPlan(n)
            groups.append(plan)
        return groups
    
    def mutate(self,list_x):
        random.seed(time.time())
        list_n = len(list_x)
        new_list = []
        u = random.randint(0, list_n - 1)
        v = random.randint(0, list_n - 1)
        
        while u == v:
            v = random.randint(0,list_n - 1)
        w = random.randint(0,list_n - 1)
        while w == u or w == v:
            w = random.randint(0,list_n - 1)

        if u > v:
            u,v = v,u
        if v > w:
            v,w = w,v
        if u > w:
            u,w = w,u
    
        """
            0~u u~v v~w w~n
            变异为：
            0~u v~w u~v w~n
        """
        for i in range(0,u):
            new_list.append(list_x[i])
        for i in range(v,w):
            new_list.append(list_x[i])
        for i in range(u,v):
            new_list.append(list_x[i])
        for i in range(w,list_n):
            new_list.append(list_x[i])
        return new_list

    
    def exchange(self,groups,n):
        random.seed(time.time())
        new_group = []
        random.seed(time.time())
        group_n = len(groups)
        
        DIV_NUM = random.randint(0,group_n - 1)
        for k in range(DIV_NUM,group_n,2):
            if k + 1 >= group_n - 2:
                break
            
            node_u = groups[k % group_n]
            node_v = groups[(k + 1) % group_n]
            
            index_u = random.randint(0,n - 1)
            index_v = random.randint(0,n - 1)
            while index_u == index_v:
                index_v = random.randint(0,n - 1)
            
            if index_u > index_v:
                index_u , index_v = index_v , index_u
            
            tmp_v = node_v[index_u:index_v]
            tmp_u = node_u[index_u:index_v]
            len_u = len_v = 0
            
            new_u = new_v = []
            
            for item in node_u:
                if len_u == index_u:
                    new_u.extend(tmp_u)
                    len_u += 1
                if item not in tmp_u:
                    new_u.append(item)
                    len_u += 1
            
            for item in node_v:
                if len_v == index_u:
                    new_v.extend(tmp_v)
                    len_v += 1
                if item not in tmp_v:
                    new_v.append(item)
                    len_v += 1
            
            new_group.append(new_u)
            new_group.append(new_v)
        
        for item in groups:
            if len(new_group) == group_n:
                break
            new_group.append(item)
        return new_group
    
    def sort_group(self,group,graph):
        # print(group)
        group_n = len(group)
        for i in range(group_n):
            for j in range(i+1,group_n):
                if graph.ask_distance_for_plan(group[i]) > graph.ask_distance_for_plan(group[j]):
                    group[i],group[j] = group[j],group[i]
        
        return group
    
    def run(self,n,graph):
        # n is the size of each individual
        init_group = self.init_group(n)
        init_group = self.sort_group(init_group,graph)
        i_time = 0
        while i_time < self.MAX_TIME:
            # print("fitness = ",graph.ask_distance_for_plan(init_group[0]))
            # print(init_group[0])
            init_group = self.exchange(init_group,n)
            for i in range(self.MAX_GROUP):
                if random.random() < self.MUTE_RATE:
                    init_group[i] = self.mutate(init_group[i])
            
            init_group = self.sort_group(init_group,graph)
            # print(init_group,"\n")
            i_time += 1
            # print("i_time = ",i_time)

    

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
    ga = GA(100,100,0.3)
    ga.run(graph.point_n,graph)
    

if __name__ == '__main__':
    main()