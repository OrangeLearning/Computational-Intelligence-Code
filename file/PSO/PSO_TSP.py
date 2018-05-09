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
import matplotlib.pyplot as mpl
from mpl_toolkits.mplot3d import Axes3D


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


class Swarm:
    def __init__(self, plan):
        self.plan = copy.copy(plan)
        self.fitness = 0.0
        self.best = 0.0
        self.best_plan = []


def cmp_speed(a):
    return a[1]


class PSO:
    def __init__(self, max_group=100, max_time=1000, c1=1, c2=1, eta=0.9, xi=0.85):
        self.MAX_TIME = max_time
        self.MAX_GROUP = max_group
        self.c1 = c1
        self.c2 = c2
        self.eta = eta
        self.xi = xi
        pass

    def init_plan(self, n):
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

    def init_group(self, n, graph):
        group = []
        for i in range(self.MAX_GROUP):
            new_plan = self.init_plan(n)

            while new_plan in group:
                new_plan = self.init_plan(n)
            group.append(new_plan)

        return group

    def run(self, n, graph):
        random.seed(time.time())
        group = self.init_group(n, graph)

        swarms = []
        for item in group:
            tmp = Swarm(item)
            tmp.fitness = graph.ask_distance_for_plan(item)
            tmp.best = graph.ask_distance_for_plan(item)
            tmp.best_plan = copy.copy(tmp.plan)
            tmp.speed = self.init_plan(n)
            swarms.append(tmp)

        i_time = 0

        swarm_best = {
            "fitness": swarms[0].fitness,
            "plan": copy.copy(swarms[0].plan)
        }

        ans_each_time = []
        while i_time < self.MAX_TIME:
            for bird in swarms:
                bird.fitness = graph.ask_distance_for_plan(bird.plan)
                if bird.fitness < bird.best:
                    bird.best_plan = copy.copy(bird.plan)
                    bird.best = bird.fitness

                if bird.best < swarm_best["fitness"]:
                    swarm_best["fitness"] = bird.best
                    swarm_best["plan"] = copy.copy(bird.plan)

            # print(swarm_best)

            temp_speed = []

            # 更新每个粒子
            for bird in swarms:
                temp_speed.clear()

                # print(bird.plan)
                eta = self.eta
                xi = self.xi

                for i in range(n):
                    if bird.plan[i] != swarm_best["plan"][i]:
                        swap_operator = (i, swarm_best["plan"].index(bird.plan[i]), eta)
                        temp_speed.append(swap_operator)
                        u = swap_operator[0]
                        v = swap_operator[1]
                        bird.plan[u], bird.plan[v] = bird.plan[v], bird.plan[u]

                for i in range(n):
                    if bird.plan[i] != bird.best_plan[i]:
                        swap_operator = (i, bird.best_plan.index(bird.plan[i]), xi)
                        temp_speed.append(swap_operator)
                        u = swap_operator[0]
                        v = swap_operator[1]
                        bird.plan[u], bird.plan[v] = bird.plan[v], bird.plan[u]

                for item in temp_speed:
                    rate = random.random()
                    if rate < item[2]:
                        # print("in")
                        u = item[0]
                        v = item[1]
                        bird.plan[u], bird.plan[v] = bird.plan[v], bird.plan[u]

                # 变异
                if bird.plan == swarm_best["plan"]:
                    u = random.randint(0, n - 1)
                    v = random.randint(0, n - 1)
                    while v == u:
                        v = random.randint(0, n - 1)
                    bird.plan[u], bird.plan[v] = bird.plan[v], bird.plan[u]
            ans_each_time.append(swarm_best["fitness"])
            i_time += 1
        print(self.eta, ' ',self.xi)
        return swarm_best, ans_each_time


def main(eta=0.0, xi=0.0):
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

    pso = PSO(80, 800, 1, 1, eta=eta, xi=xi)
    res, ans = pso.run(graph.point_n, graph)
    # mpl.plot(ans)
    # mpl.show()

    # print(res)
    # x_s = []
    # y_s = []
    # for item in res["plan"]:
    #     x_s.append(graph.points[item].x)
    #     y_s.append(graph.points[item].y)
    # x_s.append(x_s[0])
    # y_s.append(y_s[0])
    # mpl.plot(x_s,y_s,marker='o')
    # mpl.show()
    print(res)
    return res["fitness"]


if __name__ == '__main__':
    xi_s = [i / 100 for i in range(9,100,10)]
    eta_s = [i / 100 for i in range(9,100,10)]
    # main()
    z_s = []
    for xi in xi_s:
        for eta in eta_s:
            z_s.append(main(xi,eta))

    print(xi_s)
    print(eta_s)
    print(z_s)
    fig = mpl.figure()
    ax = Axes3D(fig)
    ax.plot_trisurf(xi_s,eta_s,z_s)
    mpl.show()