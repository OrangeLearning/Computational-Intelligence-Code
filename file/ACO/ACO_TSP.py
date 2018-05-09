#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 21:48:55 2018

@author: orangeluyao

ant colony

"""
import copy
import random
import math
import time
import matplotlib.pyplot as mpl

DEFAULT_ALPHA = 1.0
DEFAULT_BETA  = 2.0
DEFAULT_ROU   = 0.9
DEFAULT_Q     = 10.0

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

class Ant:
    def __init__(self,cur_city,city_n):
        self.city = cur_city
        self.tabu_table = [0 for i in range(city_n)]
        self.tabu_table[self.city] = 1
        self.city_cnt = 1
    

class ACO:
    def __init__(self,ant_n,max_time):
        self.MAX_TIME = max_time
        self.ant_n = ant_n
        self.alpha = DEFAULT_ALPHA
        self.beta = DEFAULT_BETA
        self.rou = DEFAULT_ROU
        self.Q = DEFAULT_Q
    
    def init_ants(self,city_n):
        random.seed(time.time())
        ants = []
        for i in range(self.ant_n):
            ants.append(Ant(random.randint(0,city_n-1),city_n))
        return ants
    
    def init_info(self,n):
        info = [[1.0 for i in range(n)] for i in range(n)]
        # print(info)
        return info
    
    def run(self,n,graph):
        random.seed(time.time())
        city_n = n
        i_time = 0
        info = self.init_info(n)
        new_info = copy.copy(info)
        
        ants = self.init_ants(n)

        init_plan = [i for i in range(city_n)]
        better_res = {
                "fitness": graph.ask_distance_for_plan(init_plan),
                "plan": init_plan
            }

        # print("start algorithm"," maxtime = ",self.MAX_TIME)
        while i_time < self.MAX_TIME:
            info = copy.copy(new_info)
            
            for i in range(city_n):
                for j in range(city_n):
                    if i == j:
                        continue
                    else:
                        new_info[i][j] *= (1 - self.rou)
            
            for ant in ants:
                city_i = ant.city
                p_max = 0.0
                city_max = city_i
                
                for city in range(city_n):
                    if ant.tabu_table[city] != 0:
                        continue
                    else:
                        p = math.pow(info[city_i][city],self.alpha) * math.pow((1.0 / graph.ask_distance(city_i,city)),self.beta)
                        if p_max < p:
                            p_max = p
                            city_max = city
                
                new_info[city_i][city_max] += self.Q
                ant.city_cnt += 1
                ant.tabu_table[city_max] = ant.city_cnt
                ant.city = city_max
 

                if ant.city_cnt == city_n:
                    # print(ant.city)
                    # print(ant.tabu_table)
                    plan = []
                    for i in range(city_n):
                        for j in range(city_n):
                            if i + 1 == ant.tabu_table[j]:
                                plan.append(j)
                                break

                    if better_res["fitness"] > graph.ask_distance_for_plan(plan):
                        better_res["fitness"] = graph.ask_distance_for_plan(plan)
                        better_res["plan"] = copy.copy(plan)
            
            i_time += 1
        
        # print(better_res)
        return better_res
    
def main(ant_n = 100,tim = 2000):
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

    start_time = time.time()
    aco = ACO(ant_n,tim)
    res = aco.run(graph.point_n,graph)
    end_time = time.time()

    tim = end_time - start_time
    # print(tim)

    # x_s = []
    # y_s = []
    # for i in res["plan"]:
    #     x_s.append(graph.points[i].x)
    #     y_s.append(graph.points[i].y)
    # x_s.append(x_s[0])
    # y_s.append(y_s[0])
    # mpl.plot(x_s, y_s,marker='o')
    # mpl.show()
    return res["fitness"]


    

if __name__ == '__main__':
    # main()
    sum = 0.0
    ant_n = [1,5,10,50,80,100,150,200,300,500,600,750,800,900,1000]

    ans = []
    for i in ant_n:
        res = main(100,i)
        ans.append(res)
        print(res)

    print(ans)

    mpl.plot(ant_n,ans)
    mpl.show()