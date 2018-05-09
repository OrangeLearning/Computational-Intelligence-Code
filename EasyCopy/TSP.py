import numpy as np
import matplotlib.pyplot as mpl

x_s = []
y_s = []
with open("in.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = str(line)
        # print(line)
        items = line.split(' ')
        x = float(items[1])
        y = float(items[2])
        x_s.append(x)
        y_s.append(y)

mpl.scatter(x_s,y_s)
mpl.show()