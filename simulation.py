import numpy as np
import matplotlib.pyplot as plt
import util
import pandas as pd
import datetime


runs = 1000
days = 30
data = util.read('edgelist.txt')
means = {
    'infected': [],
    'dead': [],
    'initial': []
}

start = datetime.datetime.now()
Graph = util.make_graph(data)
data = []

for i in range(10000):
    Graph1, initial = util.initialise(Graph)
    Graph1, infected, dead = util.simulate(Graph1, days)
    data.append((i, initial, infected, dead))
    means['infected'] = np.append(means['infected'], infected)
    means['dead'] = np.append(means['dead'], dead)
    means['initial'] = np.append(means['initial'], initial)
    print((i, initial, infected, dead))

end = datetime.datetime.now()
print("Time taken", end-start)

util.printf("result.txt", data)

mean = np.mean(means['infected'])
std = np.std(means['infected'])
util.printf('infected.txt', (mean, std))
print("mean infected:", mean, "- std.dev infected", std)

mean = np.mean(means['dead'])
std = np.std(means['dead'])
util.printf('dead.txt', (mean, std))
print("mean dead:", mean, "- std.dev dead", std)

mean = np.mean(means['initial'])
std = np.std(means['initial'])
util.printf('initial.txt', (mean, std))
print("mean initial:", mean, "- std.dev initial", std)
