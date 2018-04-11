from GeneticAlgorithmBasic import BasicNode
from GeneticAlgorithmBasic import BasicGroup


import GeneticAlgorithmTool as gat
from TSP import Graph
from TSP import Point
import TSP
import random
import time

# 随机一个排列
def random_vector(n):
    random.seed(time.time())
    vec = []
    for i in range(n):
        vec.append(i)

    for i in range(n):
        tt = random.randint(0,n-1)
        while tt == i:
            tt = random.randint(0,n-1)
        vec[i],vec[tt] = vec[tt],vec[i]
    print(vec)

    return vec

def random_node(graph,n):
    return BasicNode(n,random_vector(n),graph,TSP.ask_sum_distance)


def build_graph():
    graph = Graph()
    with open("data.in","r") as f:
        lists = f.readlines()
        for item in lists:
            if item[0] == "#":
                break
            ss = item.split(" ")
            graph.add_point(Point(float(ss[1]),float(ss[2]),ss[0]))

    gs = [[] for i in range(graph.point_n)]
    for i in range(graph.point_n):
        gs[i] = []
        for j in range(graph.point_n):
            gs[i].append(TSP.ask_distance(graph.points[i], graph.points[j]))

    return graph,gs

def main():
    random.seed(time.time())
    # 构造图
    graph,gs = build_graph()

    GA_NUM = 50
    GA_TIMES = 100
    GA_MUTE = 0.1
    
    """
        准备开始搜索
        
        实际就是得到一种排列
    """
    group = BasicGroup(GA_NUM)

    print("start ga")

    print("init")
    for i in range(GA_NUM):
        group.add_Node(random_node(graph,graph.point_n))
        print(group.group_n)

    print("------------------")
    ans = group.genetic_algorithm(GA_TIMES=GA_TIMES,
                            GA_MUTE=GA_MUTE,
                            ask_fitness=TSP.ask_sum_distance,
                            exchange=gat.my_exchange,
                            mutate=gat.my_mutate,
                            graph=graph,
                            vector_n=graph.point_n)
    print("------------ans--------------")
    print(ans.fitness)
    # group.genetic_algorithm(GA_TIMES,GA_MUTE,TSP.cmp_list,gat.my_exchange,gat.my_mutate,group.group_n)

if __name__ == '__main__':
    main()
