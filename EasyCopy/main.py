import matplotlib.pyplot as mpl
res = [5, 17, 3, 19, 7, 15, 11, 16, 8, 12, 18, 14, 9, 6, 1, 4, 2, 10, 13, 0]
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

x_s = []
y_s = []
for item in res:
    x_s.append(graph.points[item])
    y_s.append(graph.points[item])

x_s.append(x_s[0])
y_s.append(y_s[0])
mpl.plot(x_s,y_s)
mpl.show()