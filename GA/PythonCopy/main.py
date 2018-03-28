from GeneticAlgorithmBasic import BasicNode
from GeneticAlgorithmBasic import BasicGroup

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
        vec[i],vec[tt] = vec[tt],vec[i]
    print(vec)

    return vec

def random_node(n):
    return BasicNode(n,random_vector(n),TSP.ask_sum_distance)


def build_graph():
    graph = Graph()
    with open("data.in","r") as f:
        lists = f.readlines()
        for item in lists:
            ss = item.split(" ")
            graph.add_point(Point(float(ss[1]),float(ss[2]),ss[0]))

    gs = [[] for i in range(graph.point_n)]
    for i in range(graph.point_n):
        gs[i] = []
        for j in range(graph.point_n):
            gs[i].append(TSP.ask_distance(graph.points[i], graph.points[j]))

    return graph,gs

def main():
    # 构造图
    graph,gs = build_graph()

    GA_NUM = 50
    GA_TIMES = 100
    """
        准备开始搜索
        
        实际就是得到一种排列
    """
    group = BasicGroup(GA_NUM)
    for i in range(GA_NUM):
        group.add_Node(random_node(graph.point_n))

    group.genetic_algorithm(GA_TIMES,TSP.cmp_list)


if __name__ == '__main__':
    main()