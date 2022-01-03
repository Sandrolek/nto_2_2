#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Чтобы показывался график надо установить GUI компонент, например Qt5 и вызвать matplotlib.pyplot.show()
# pip install PyQt5

import networkx as nx
#import matplotlib.pyplot as plt
#import dimod
import math

from networkx.algorithms.shortest_paths.generic import shortest_path

n = 7
STEPS = 50
BATTERY = 24
COST = 1200

map = [ ['.', '.', '.', '.', '.', '.'],
        ['.', '#', '#', '#', '#', '.'],
        ['.', '.', '#', '.', '#', '.'],
        ['.', '.', '#', '.', '#', '.'],
        ['.', '#', '#', '#', '#', '.'],
        ['.', '.', '.', '.', '.', '.'],
]

# n = int(input())
# STEPS = int(input())
# BATTERY = int(input())
# COST = int(input())

# map = [['.' for j in range(n-1)] for i in range(n-1)]

# for i in range(1, n-2):
#     map[i] = list('.' + input() + '.')

#print(map)

check = [[0, -1], [-1, 0], [0, 1], [1, 0]]

#tsp = traveling_salesman_problem

def num_of_drones(G):
    #print("Counting num drones")
    #print(tsp(G))
    #len_path = len(tsp(G)) - 1
    #print(len_path)
    #res = math.ceil(2 * len_path / BATTERY)
    #print(f"NumDrones is: {res}")
    return 2

class Drone:

    def __init__(self, pos=(0, 0), batt=1, num=0):
        self.pos = pos
        self.batt = batt
        self.num = num

    def search(self, G, node): # find destination
        
        print(f"Num: {self.num}, Len: {len(nx.shortest_path(G, source=self.pos, target=(0,0))) - 1}, Batt: {self.batt}")

        if (self.batt <= len(nx.shortest_path(G, source=self.pos, target=(0,0))) - 1 ):
            node = (0,0)

        #print(f"Navigating dron {self.num} from {self.pos} to {node}")
        path = shortest_path(G, source=self.pos, target=node)
        #print(path)

        res = self.command(self.pos, path[1])

        self.pos = path[1]

        self.batt -=1

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
        #self.drones[num]
        # for i in range(self.num):
        #     self.drones[i] = Drone(batt=BATTERY, num = i)

        self.drones = [Drone(batt=BATTERY, num = i) for i in range(self.num)]
        
        # print(f"Drones:")
        # for drone in self.drones:
        #     print(drone.num, drone.pos, drone.batt)

    def update(self):
        self.update_map()
        res = self.update_drones()
        #print(f"RES1: {res}")

        self.return_commands()
        
        #self.draw_graph()

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
        #print(l)
        
        res = ""

        for i, drone in enumerate(self.drones):
            res += drone.search(G, l[i][0])

        return res

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

#rint("Edges:")  
#print(G.edges())
#print("Vertices:")  
#print(G.nodes())

num_drones = num_of_drones(G)

print(num_drones)

fleet = Fleet(G, num_drones, (0, 0), BATTERY)

for _ in range(STEPS):

    print(f"{fleet.update()}")
