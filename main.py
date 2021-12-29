#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib

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

def num_of_drones(G):
    return 2

class Drone:

    def __init__(self, pos=(0, 0), batt=1):
        self.pos = pos
        self.batt = batt

    def search(self): # find destination
        pass

    def command(self): # return command for drone
        pass

class Fleet:

    def __init__(self, G, num, pos, batt):
        self.G = G
        self.num = num
        self.drones = [Drone(pos, batt)] * self.num
        print(f"Drones:")
        for drone in self.drones:
            print(drone.pos, drone.batt)

    def update(self): # call search for each drone
        for drone in self.drones:
            drone.search()

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

print("Edges:")  
print(G.edges())
print("Vertices:")  
print(G.nodes())

nx.draw(G)

num_drones = num_of_drones(G)

fleet = Fleet(G, num_drones, (0, 0), BATTERY)

for _ in range(STEPS):
    fleet.update()

