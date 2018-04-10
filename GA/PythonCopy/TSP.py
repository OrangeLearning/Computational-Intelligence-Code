import math
class Point:
    def __init__(self,x,y,id):
        self.x = x
        self.y = y
        self.id = id

class Graph:
    def __init__(self):
        self.point_n = 0
        self.points = []

    def add_point(self,point):
        self.point_n += 1
        self.points.append(point)

    def show(self):
        for item in self.points:
            print(item.x," ",item.y," ",item.id)


def ask_distance(a,b):
    return math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y))

def ask_sum_distance(list_x,graph):
    i = 1
    list_len = len(list_x)
    sum = 0.0
    while i < list_len:
        sum += ask_distance(graph.points[list_x[i-1]],graph.points[list_x[i]])
        i += 1
    return sum

def cmp_list(list_a,list_b):
    return ask_sum_distance(list_a) < ask_sum_distance(list_b)