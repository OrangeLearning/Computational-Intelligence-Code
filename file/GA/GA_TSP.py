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
import matplotlib.pyplot as mpl


def sqr(x):
    return x * x


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Graph:
    def __init__(self, n):
        self.points = []
        self.point_n = n

    def add_point(self, p):
        self.points.append(p)
        self.point_n += 1

    def ask_distance(self, i, j):
        point_x = self.points[i]
        point_y = self.points[j]
        return math.sqrt(sqr(point_x.x - point_y.x) + sqr(point_x.y - point_y.y))

    def ask_distance_for_plan(self, plan):
        res = 0.0
        for i in range(1, self.point_n):
            res += self.ask_distance(plan[i], plan[i - 1])
        res += self.ask_distance(plan[0], plan[self.point_n - 1])
        # print(plan,' ',res)
        return res

    def show(self):
        for item in self.points:
            print(item.x, " ", item.y)


class Gen:
    def __init__(self):
        self.fitness = 0.0
        self.plan = []


class GA:
    def __init__(self, max_time, max_group, exchange_rate, mute_rate):
        self.MAX_TIME = max_time
        self.MAX_GROUP = max_group
        self.EXCHANGE_RATE = exchange_rate
        self.MUTE_RATE = mute_rate

    # 初始化一个序列作为初始数据
    def initPlan(self, n):
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

    def init_group(self, n):
        groups = []
        for i in range(self.MAX_GROUP):
            plan = self.initPlan(n)
            while plan in groups:
                plan = self.initPlan(n)
            groups.append(plan)
        return groups

    def mutate(self, list_x):
        random.seed(time.time())
        n = len(list_x)
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        while v == u:
            v = random.randint(0, n - 1)
        list_x[u], list_x[v] = list_x[v], list_x[u]
        return list_x

    def exchange(self, parent1, parent2):
        index1 = random.randint(0, len(parent1) - 1)
        index2 = random.randint(index1, len(parent1) - 1)
        # print(parent1[index1:index2])
        tempGene = parent2[index1:index2]  # 交叉的基因片段
        newGene = []
        p1len = 0
        for g in parent1:
            if p1len == index1:
                newGene.extend(tempGene)  # 插入基因片段
                p1len += 1
            if g not in tempGene:
                newGene.append(g)
                p1len += 1
        return newGene

    def sort_group(self, group, graph):
        # print(group)
        group_n = len(group)
        for i in range(group_n):
            for j in range(i + 1, group_n):
                if graph.ask_distance_for_plan(group[i]) > graph.ask_distance_for_plan(group[j]):
                    group[i], group[j] = group[j], group[i]

        return group

    def run(self, n, graph):
        # n is the size of each individual
        init_group = self.init_group(n)
        # init_group = self.sort_group(init_group, graph)
        i_time = 0
        best_ans = {
            "fitness": graph.ask_distance_for_plan(init_group[0]),
            "plan": init_group[0]
        }
        # print(init_group)
        ans_each = []
        while i_time < self.MAX_TIME:
            # print(best_ans)

            # init_group = self.sort_group(init_group, graph)

            for i in range(self.MAX_GROUP):
                if random.random() < self.EXCHANGE_RATE:
                    j = random.randint(0, self.MAX_GROUP - 1)
                    while i == j:
                        j = random.randint(0, self.MAX_GROUP - 1)
                    new_plan = self.exchange(init_group[i], init_group[j])
                    init_group[i] = copy.copy(new_plan)

                if random.random() < self.MUTE_RATE:
                    init_group[i] = self.mutate(init_group[i])

                if graph.ask_distance_for_plan(init_group[i]) < best_ans["fitness"]:
                    best_ans["fitness"] = graph.ask_distance_for_plan(init_group[i])
                    best_ans["plan"] = copy.copy(init_group[i])

            ans_each.append(best_ans["fitness"])
            i_time += 1

        return best_ans,ans_each


def main(group_n = 100,mute = 0.3):
    graph = Graph(0)
    with open("in.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = str(line)
            # print(line)
            items = line.split(' ')
            x = float(items[1])
            y = float(items[2])
            # print('x =',x,' y = ',y)
            graph.add_point(Point(x, y))
    ga = GA(500, group_n, 1.0, mute)
    # res,ans = ga.run(graph.point_n, graph)
    res = {'fitness': 301.1644602573964, 'plan': [5, 17, 3, 19, 7, 15, 11, 16, 8, 12, 18, 14, 9, 6, 1, 4, 2, 10, 13, 0]}
    # res = [5, 17, 3, 19, 7, 15, 11, 16, 8, 12, 18, 14, 9, 6, 1, 4, 2, 10, 13, 0]
    # 结果展示
    x_s = []
    y_s = []
    for i in res["plan"]:
        x_s.append(graph.points[i].x)
        y_s.append(graph.points[i].y)
    x_s.append(x_s[0])
    y_s.append(y_s[0])
    mpl.plot(x_s,y_s,marker='o')
    mpl.show()
    return res["fitness"]


if __name__ == '__main__':
    # mute_s = [item / 100 for item in range(0,100,5)]
    # s = []
    # group_n_s = [100,200,300,400,500,600,700,800,900,1000]
    # for item in group_n_s:
    #     s.append(main(item))
    #     print(len(s))
    # mpl.plot(group_n_s,s)
    # mpl.show()
    main()
