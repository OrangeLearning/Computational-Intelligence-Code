import random

"""
    基础的单个个体类

"""
class BasicNode:
    def __init__(self,vector_n,vector,graph,ask_fitness):
        self.vector_n = vector_n
        self.vector = vector
        self.fitness = ask_fitness(vector,graph)

    def show(self):
        print("vector_n = ",self.vector_n)
        print("vector : \n",self.vector)
        print("fitness = ",self.fitness)
"""
    基础的群体类
"""
class BasicGroup:
    def __init__(self,cnt = 0):
        # 变量
        self.group_n = cnt
        self.groups = []

    def add_Node(self,node):
        self.groups.append(node)


    """
        通用的遗传算法
            GA_TIMES 就是设置迭代次数
            ask_fitness 排序函数
            judge_cmp 结束标志 非必须
            exchange 表示交叉
            mutate 变异
    """
    def genetic_algorithm(self,graph,GA_TIMES,GA_MUTE,ask_fitness,exchange,mutate,vector_n,judge_end=None):
        if self.group_n != len(self.groups):
            return "init failed"

        self.groups.sort(key=lambda x:(x.fitness))
        # 迭代次数
        for time_i in range(GA_TIMES):

            print("time_i = ",time_i," ans = ",self.groups[0].fitness)
            for item in self.groups:
                print(item.fitness,end=" ")
            print("")
            # for item in self.groups:
            #     item.show()
            # 有些框架中需要judge_end作为找到最佳值的结束符号
            # 有些不知道最佳值的情况就可以无所谓

            if judge_end != None:
                if judge_end(self.groups):
                    break
            self.groups = exchange(self.groups,self.group_n,vector_n)
            print(self.groups[0].vector)

            for i in range(self.group_n):
                if random.random() < GA_MUTE:
                    self.groups[i].vector = mutate(self.groups[i].vector)

            for item in self.groups:
                item.fitness = ask_fitness(item.vector,graph)
            self.groups.sort(key=lambda x: (x.fitness))
        return self.groups[0]