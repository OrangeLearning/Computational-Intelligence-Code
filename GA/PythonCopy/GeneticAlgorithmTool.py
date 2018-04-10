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

    if u > v:
        u,v = v,u
    if v > w:
        v,w = w,v
    if u > w:
        u,w = w,u

    """
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

# 交叉
def my_exchange(group,vector_n):
    new_group = []
    GA_DIV = random.randint(0,vector_n - 1)

    for k in range(0,group.group_n,step=2):
        if k + 1 >= group.group_n:
            break

        # 交叉的两个变量
        node_u = group[k]
        node_v = group[k+1]

        for i in range(GA_DIV,vector_n):
            node_u.vector[i],node_v.vector[i] = node_v.vector[i],node_v.vector[i]

        # 下面解决冲突：
        cnt_u = [0 for i in range(0,vector_n)]
        cnt_v = [0 for i in range(0,vector_n)]

        for i in range(0,vector_n):
            cnt_u[node_u.vector[i]] += 1
            cnt_v[node_v.vector[i]] += 1


        uu = []
        vv = []

        for i in range(0,vector_n):
            if cnt_u[i] == 2:
                uu.append(node_u.vector[i])
            if cnt_v[i] == 2:
                vv.append(node_v.vector[i])

        pu = pv = 0
        for i in range(0,vector_n):
            if cnt_u[node_u.vector[i]] == 2:
                node_u.vector[i] = vv[pv]
                pv += 1
            if cnt_v[node_v.vector[i]] == 2:
                node_v.vector[i] = uu[pu]
                pu += 1

        new_group.append(node_u)
        new_group.append(node_v)
    
    return new_group
