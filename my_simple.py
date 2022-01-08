#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
import math
import numpy

#from networkx.algorithms.cycles import recursive_simple_cycles
#from networkx.algorithms.shortest_paths.unweighted import all_pairs_shortest_path_length

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
      
n = int(input())
STEPS = int(input())
BATTERY = int(input())
COST = int(input())

size = n - 3

dirs = {(-1, 0): 'U',
        (0, 1): 'R',
        (1, 0): 'D',
        (0, -1): 'L'}

input_map = [['.' for j in range(size)] for i in range(size)]

for i in range(size):
    input_map[i] = list(input())

start_time = time()

#print(f"MAP: {input_map}")

class Drone():
    def __init__(self, last_map, neighbours):
        self.batt = BATTERY
        self.all_path = ''
        self.cur_path = ''
        self.coords = [0, 0]
        self.last_map = last_map
        self.neighbours = neighbours

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

    def reverse(self, ddir):
        if dir == 'U':
            return 'D'
        elif dir == 'D':
            return 'U'
        elif dir == 'L':
            return 'R'
        elif dir == 'R':
            return 'L'
        return 'I'

    def calc_coords(self, curCoords, dir):
        if dir == 'U':
            curCoords[0] -= 1
        elif dir == 'D':
            curCoords[0] += 1
        elif dir == 'L':
            curCoords[1] -= 1
        elif dir == 'R':
            curCoords[1] += 1
        elif dir == 'I':
            pass
        return curCoords

    def search(self):
        cur_neighbours = self.neighbours[tuple(self.coords)]
        target = min(cur_neighbours, key=lambda x: self.last_map[x[0]][x[1]])
        dir = self.command(self.coords, target)

        self.all_path += dir
        self.cur_path += dir
        self.batt -= 1

        self.coords = target

        self.last_map[self.coords[0]][self.coords[1]] += 1


        print(f"CUR Pos: {self.coords}, batt: {self.batt}")

        if self.coords == [0, 0]:
            self.batt = BATTERY
            self.cur_path = ''

    def return_to_base(self):
        last_move = self.cur_path[-1]
        rev_dir = self.reverse(last_move)

        self.all_path += rev_dir
        self.cur_path = self.cur_path[:len(self.cur_path) - 1]
        
        self.batt -= 1
        self.coords = self.calc_coords(self.coords, rev_dir)

        print(f"Batt: {self.batt}, coords: {self.coords}, rev_dir: {rev_dir}, path: {self.cur_path}")

        #self.coords = calcCoords(self.coordinates, rev_dir)
        
        self.last_map[self.coords[0]][self.coords[1]] += 1


        if self.coords == [0, 0]:
            self.batt = BATTERY

#print("EEE")

neighbours = {}
count_last = numpy.zeros([size, size], dtype=int)

for i in range(size):
    for j in range(size):
        if input_map[i][j] == '#':
            print(f"Node: {(i, j)}")
            for dir in dirs:
                if 0 <= i + dir[0] < size and 0 <= j + dir[1] < size:
                    if input_map[i + dir[0]][j + dir[1]] == '#':
                        print(f"\tNeigbour: {(i + dir[0], j + dir[1])}")
                        if (i, j) in neighbours:
                            neighbours[(i, j)].append([i + dir[0], j + dir[1]])
                        else:
                            neighbours[(i, j)] = [[i + dir[0], j + dir[1]]]
        else:
            count_last[i][j] = -1

for node in neighbours:
    print(f"node: {node}, neighbours: {neighbours[node]}")

num_drones = math.ceil(len(neighbours) // (BATTERY // 2))**2

print(f"NUM: {num_drones}")
print(f"count_last: {count_last}")
print(neighbours)

drones = [Drone(count_last, neighbours) for i in range(num_drones)]

for i in range(STEPS):
    for num, drone in enumerate(drones):
        print(f"Path: {drone.cur_path}")
        print(f"Pos: {drone.coords}, batt: {drone.batt}")
        print(count_last)     
        
        if drone.batt > BATTERY // 2:
            print(f"Step: {i}, Drone: {num}")
            
            drone.search()
            # dir = findDirection(drone)
            # drone.move([dir[0], dir[1]], dir[2])
        else:
            print("Returning")
            drone.return_to_base()

print(num_drones)
for i in range(STEPS):
    for drone in drones:
        print(drone.all_path[i], end='')
    print()