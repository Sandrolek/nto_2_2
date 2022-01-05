#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from time import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation


"""
7
50
24
1200
####
.#.#
.#.#
####
"""

"""
13
300
150
1200
##########
...#...#.#
...#...#.#
...#####.#
...#.....#
...##...##
....##.##.
.....###..
......#...
..#######.
"""

"""
35
2000
4000
1500
################################
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
..#...#...#...#...#...#...#...#
.##..##..##..##..##..##..##..##.
.#...#...#...#...#...#...#...#..
.##..##..##..##..##..##..##..##.
################################
"""

n = int(input())
STEPS = int(input())
BATTERY = int(input())
COST = int(input())

map = [['.' for j in range(n-1)] for i in range(n-1)]

for i in range(1, n-2):
    map[i] = list('.' + input() + '.')

start_time = time()

check = [[0, -1], [-1, 0], [0, 1], [1, 0]]

def  num_of_drones(G):
    #print("Counting num drones")
    
    NODES_COUNT = len(G.nodes())
    
    loss_0 = STEPS * (STEPS ** 2) / 2
    loss_1 = 0

    for t in range(STEPS, 0, -1):
        loss_1 += t * (NODES_COUNT - (t - STEPS) - 1) / NODES_COUNT
    
    #print(loss_0, loss_1)

    loss = loss_0
    for i in range(20):
        next_loss = loss - loss_1 / (2 ** i) + COST
        if (next_loss > loss):
            break
        loss = next_loss
        #print(i + 1, loss)

    return i

class Drone:

    def __init__(self, pos=(0, 0), batt=1, num=0):
        self.pos = pos
        self.batt = batt
        self.num = num

    def search(self, G, node): # find destination
        
        #print(f"Num: {self.num}, Len: {len(nx.shortest_path(G, source=self.pos, target=(0,0))) - 1}, Batt: {self.batt}")

        if (self.batt < len(G.nodes[self.pos]["start_path"])):
            path = G.nodes[self.pos]["start_path"]
        else:
            path = nx.shortest_path(G, source=self.pos, target=node)

        #print(f"Navigating dron {self.num} from {self.pos} to {node}")
        
        #print(path)

        if (len(path) > 1):
            next_node = path[1]
        else:
            #print(f"problem, source: {self.pos}, Target: {node}")
            #next_node = path[0]
            next_node = nx.neighbors(G, self.pos)[0]

        res = self.command(self.pos, next_node)

        self.pos = next_node

        self.batt -= 1

        if (self.pos == (0,0)):
            self.batt = BATTERY

        return res

    def command(self, pos, target): # return command for drone
        y0, x0 = pos
        y1, x1 = target

        #print(f"y0: {y0}, x0: {x0}, y1: {y1}, x1: {x1}")
        
        res = '' 

        if (y0 < y1):
            res = 'D'
        elif (y0 > y1):
            res = 'U'
        elif (x0 < x1):
            res = 'R'
        elif (x0 > x1):
            res = 'L'

        return res

class Fleet:

    def __init__(self, G, num, pos, batt):
        self.G = G
        self.num = num

        self.drones = [Drone(batt=BATTERY, num = i) for i in range(self.num)]

        

        start_paths = nx.shortest_path(G, target=(0, 0))
        for node, start_path in start_paths.items():
            self.G.nodes[node]['start_path'] = start_path

    def update(self):
        self.update_map()
        res = self.update_drones()

        return res

    def update_map(self):
        for i in G.nodes:
            G.nodes[i]['in'] = False
            G.nodes[i]['num'] = -1

        for i, drone in enumerate(self.drones):
            self.G.nodes[drone.pos]['in'] = True
            G.nodes[drone.pos]['num'] = i
            self.G.nodes[drone.pos]['last'] = 0

        #print("data:")
        for i in self.G.nodes.data():
            if (i[1]['in'] == False):
                self.G.nodes[i[0]]['last'] += 1
            #print(i)
    
    def update_drones(self): # call search for each drone
        #print("L:")
        l = sorted(self.G.nodes.data(), key=lambda x: x[1]['last'], reverse=True)
        #print(f"type: {type(l)} L: {l}")
        #for i in l:
        #    print(i)
        
        res = ""

        for i, drone in enumerate(self.drones):
            #print(f"Drone: {drone.num}, batt: {drone.batt}")
            
            #print(f"i: {i}, drone: {drone}, l: {l[i]}res: {res}")
            res += drone.search(G, l[i][0])

        return res

G = nx.Graph()

for i, str in enumerate(map):
    for j, symb in enumerate(str):

        if symb == '#':
            # print(i, j, end=' ')
            # print(symb)
            for k in check:
                # print(f"New: {i + k[0]}, {j + k[1]}")
                # print(f"New Symb: {map[i + k[0]][j + k[1]]}")
                if map[i + k[0]][j + k[1]] == '#':
                    G.add_edge((i-1, j-1), (i + k[0]-1, j + k[1]-1))
                    G.nodes[(i-1, j-1)]['last'] = 0
                    G.nodes[(i + k[0]-1, j + k[1]-1)]['last'] = 0

#rint("Edges:")  
#print(G.edges())
#print("Vertices:")  
#print(G.nodes())

num_drones = num_of_drones(G)

print(num_drones)

fleet = Fleet(G, num_drones, (0, 0), BATTERY)

res = ""

for _ in range(STEPS):
    res += fleet.update()
    res += '\n'
    #print(f"{fleet.update()}")

fig, ax = plt.subplots()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)


def animate(i):
    """анимируем движение дронов"""

    ax.clear()
    options = {
        "font_size": 24,
        "node_size": 3000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5,
    }
    # options = {
    #     "font_size": 12,
    #     "node_size": 1000,
    #     "node_color": "white",
    #     "edgecolors": "black",
    #     "linewidths": 2,
    #     "width": 2,
    # }
    # options = {
    #     "font_size": 6,
    #     "node_size": 100,
    #     "node_color": "white",
    #     "edgecolors": "black",
    #     "linewidths": 1,
    #     "width": 1,
    # }
    labels = {}
    for inx, drone in enumerate(fleet.drones):
        labels[drone.pos] = labels.get(drone.pos, []) + [inx]
    nx.draw(
        fleet.G,
        ax=ax,
        pos={node: (node[1], -node[0]) for node in fleet.G.nodes},
        labels=labels,
        **options
    )
    if i > 0:
        fleet.update()

# # создаем гифку с анимацией движения дронов
drons_anima = animation.FuncAnimation(fig, func=animate, frames=range(STEPS + 1))
drons_anima.save("drons_anima2.gif", writer="imagemagick", fps=3)

print(res)

print(f"%s seconds", time() - start_time)
print(f"Num: {num_drones}")
