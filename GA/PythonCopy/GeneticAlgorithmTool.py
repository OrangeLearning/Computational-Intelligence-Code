"""
    This is the GA Tool file
"""
from GeneticAlgorithmBasic import BasicNode
import copy
import random

# 倒位变异
def my_mutate(list_x):
    list_n = len(list_x)
    new_list = []

    u = random.randint(0, list_n - 1)
    v = random.randint(0, list_n - 1)
    while u == v:
        v = random.randint(0,list_n - 1)

    w = random.randint(0,list_n - 1)
    while w == u or w == v:
        w = random.randint(0,list_n - 1)

    # print("u,v,w = ",u,v,w)
    if u > v:
        u,v = v,u
    if v > w:
        v,w = w,v
    if u > w:
        u,w = w,u

    # print("u,v,w = ",u,v,w)
    """
        0~u u~v v~w w~n
        变异为：
        0~u v~w u~v w~n
    """
    # print(new_list)
    for i in range(0,u):
        new_list.append(list_x[i])

    # print(new_list)
    for i in range(v,w):
        new_list.append(list_x[i])

    # print(new_list)
    for i in range(u,v):
        new_list.append(list_x[i])

    # print(new_list)
    for i in range(w,list_n):
        new_list.append(list_x[i])

    # print(new_list)
    return new_list

# 交叉
def my_exchange(group,group_n,vector_n):
    # print("len = ",len(group)," group_n = ",group_n)

    new_group = []
    GA_DIV = random.randint(0,group_n - 1)

    for k in range(GA_DIV,group_n,2):
        if k + 1 >= group_n-2:
            break
        # 交叉的两个变量
        node_u = group[k % group_n]
        node_v = group[(k + 1) % group_n]
        index_u = random.randint(0,vector_n-1)
        index_v = random.randint(0,vector_n-1)
        while index_u == index_v:
            index_v = random.randint(0,vector_n-1)

        if index_u > index_v:
            index_u,index_v = index_v,index_u

        tmp_v = node_v.vector[index_u:index_v]
        tmp_u = node_u.vector[index_u:index_v]
        len_u = len_v = 0

        new_u = copy.copy(node_u)
        new_u.vector = []
        new_v = copy.copy(node_v)
        new_v.vector = []

        for item in node_u.vector:
            if len_u == index_u:
                new_u.vector.extend(tmp_u)
                len_u += 1
            if item not in tmp_u:
                new_u.vector.append(item)
                len_u += 1

        for item in node_v.vector:
            if len_v == index_u:
                new_v.vector.extend(tmp_v)
                len_v += 1
            if item not in tmp_v:
                new_v.vector.append(item)
                len_v += 1
        new_group.append(new_u)
        new_group.append(new_v)

    for item in group:
        if len(new_group) == group_n:
            break
        new_group.append(item)
    return new_group
