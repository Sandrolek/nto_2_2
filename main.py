#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import dimod
import math
import own_tsp

from networkx.algorithms.shortest_paths.generic import shortest_path

### CONSTANTS ###

n = 8
STEPS = 50
BATTERY = 24
COST = 1200

map = [ ['.', '.', '.', '.', '.', '.', '.'],
        ['.', '#', '.', '#', '#', '.', '.'],
        ['.', '#', '#', '#', '.', '.', '.'],
        ['.', '.', '#', '#', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '#', '.'],
        ['.', '#', '.', '#', '#', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.'],
]

# map = [ ['.', '.', '.', '.', '.'],
#         ['.', '#', '#', '#', '.'],
#         ['.', '.', '.', '#', '.'],
#         ['.', '#', '#', '#', '.'],
#         ['.', '.', '.', '.', '.']
# ]

### CONSTANTS ###

### INPUT ###

# n = int(input())
# STEPS = int(input())
# BATTERY = int(input())
# COST = int(input())

# map = [['.' for j in range(n-1)] for i in range(n-1)]

# for i in range(1, n-2):
#     print(i)
#     map[i] = list('.' + input() + '.')

# print(map)

### INPUT ###

check = [[0, -1], [-1, 0], [0, 1], [1, 0]]

def  num_of_drones(G):
    print("Counting num drones")
    
    NODES_COUNT = len(G.nodes())
    
    loss_0 = STEPS * (STEPS ** 2) / 2
    loss_1 = 0

    for t in range(STEPS, 0, -1):
        loss_1 += t * (NODES_COUNT - (t - STEPS) - 1) / NODES_COUNT
    
    print(loss_0, loss_1)

    loss = loss_0
    for i in range(20):
        next_loss = loss - loss_1 / (2 ** i) + COST
        if (next_loss > loss):
            break
        loss = next_loss
        print(i + 1, loss)

    return (i, loss)

class Drone:

    def __init__(self, pos=(0, 0), batt=1, num=0):
        self.pos = pos
        self.batt = batt
        self.num = num

    def search(self, G, node): # find destination

        if (len(nx.shortest_path(G, source=self.pos, target=(0,0))) >=  self.batt):
            node = (0,0)

        print(f"Navigating dron {self.num} from {self.pos} to {node}")
        path = shortest_path(G, source=self.pos, target=node)
        print(path)

        res = self.command(self.pos, path[1])

        self.pos = path[1]

        if (self.pos == (0,0)):
            self.batt = BATTERY

        return res

    def command(self, pos, target): # return command for drone
        y0, x0 = pos
        y1, x1 = target

        print(f"y0: {y0}, x0: {x0}, y1: {y1}, x1: {x1}")
        
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
        #self.drones[num]
        # for i in range(self.num):
        #     self.drones[i] = Drone(batt=BATTERY, num = i)

        self.drones = [Drone(batt=BATTERY, num = i) for i in range(self.num)]
        
        print(f"Drones:")
        for drone in self.drones:
            print(drone.num, drone.pos, drone.batt)

    def update(self):
        self.update_map()
        res = self.update_drones()
        print(f"RES1: {res}")

        self.return_commands()
        
        self.draw_graph()

        return res

    def update_map(self):
        for i in G.nodes:
            G.nodes[i]['in'] = False
            G.nodes[i]['num'] = -1

        for i, drone in enumerate(self.drones):
            self.G.nodes[drone.pos]['in'] = True
            G.nodes[drone.pos]['num'] = i
            self.G.nodes[drone.pos]['last'] = 0

        print("data:")
        for i in self.G.nodes.data():
            if (i[1]['in'] == False):
                self.G.nodes[i[0]]['last'] += 1
            print(i)
    
    def update_drones(self): # call search for each drone
        print("L:")
        l = sorted(self.G.nodes.data(), key=lambda x: x[1]['last'], reverse=True)
        #print(l)
        
        res = ""

        for i, drone in enumerate(self.drones):
            res += drone.search(G, l[i][0])

        return res

    def draw_graph(self):
        print("Drawing Graph")

        labels_dict = {}
        for node in self.G.nodes():
            x, y = node
            z = 666
            #print(f"X: {type(x)}, Y: {y}")
            res = f"{x},{y} L: {G.nodes[node]['last']} D: {G.nodes[node]['num']}"
            labels_dict[node] = res

        nx.draw(G, labels=labels_dict, with_labels=True)

        plt.show()

    def return_commands(self): # return commands for each drone
        pass

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

print("Edges:")  
print(G.edges())
print("Vertices:")  
print(G.nodes())

print("Paths:")

print([p for p in nx.all_shortest_paths(G, source=(0, 0), target=(0, 0))])

num_drones, final_loss = num_of_drones(G)

print(final_loss, num_drones)

input()

fleet = Fleet(G, num_drones, (0, 0), BATTERY)

for _ in range(STEPS):

    print(f"{fleet.update()}")
