#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Чтобы показывался график надо установить GUI компонент, например Qt5 и вызвать matplotlib.pyplot.show()
# pip install PyQt5

import networkx as nx
import matplotlib.pyplot as plt
import dimod
import math

from networkx.algorithms.shortest_paths.generic import shortest_path

# n = int(input) - 3
# STEPS = int(input)
# BATTERY = int(input)
# COST = int(input)

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

check = [[0, -1], [-1, 0], [0, 1], [1, 0]]

tsp = nx.approximation.traveling_salesman_problem

def num_of_drones(G):
    print("Counting num drones")
    print(tsp(G))
    len_path = len(tsp(G)) - 1
    print(len_path)
    res = math.ceil(2 * len_path / BATTERY)
    print(f"NumDrones is: {res}")
    return res

class Drone:

    def __init__(self, pos=(0, 0), batt=1, num=0):
        self.pos = pos
        self.batt = batt
        self.num = num

    def search(self, G, node): # find destination
        print(f"Navigating dron {self.num} from {self.pos} to {node}")
        path = shortest_path(G, source=self.pos, target=node)
        print(path)
        self.pos = path[1]

    def command(self): # return command for drone
        pass

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
        self.update_drones()

    
    def update_map(self):
        for i in G.nodes:
            G.nodes[i]['in'] = False

        for drone in self.drones:
            self.G.nodes[drone.pos]['in'] = True
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
        
        for i, drone in enumerate(self.drones):
            drone.search(G, l[i][0])

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

num_drones = num_of_drones(G)

fleet = Fleet(G, num_drones, (0, 0), BATTERY)

for _ in range(STEPS):

    fleet.update()

pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                       node_color = [0.5 for i in G.nodes()], node_size = 500)

nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=False)

#nx.draw(G)
plt.show()