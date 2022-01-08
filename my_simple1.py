'''
7
50
24
1200
####
.#.#
.#.#
####
'''

import numpy
import math

from time import time

n = int(input())
size = n - 3
STEPS = int(input())
BATTERY = int(input())
COST = int(input())

dirs = {(-1, 0): 'U',
        (0, 1): 'R',
        (1, 0): 'D',
        (0, -1): 'L'}

input_map = [['.' for j in range(size)] for i in range(size)]

for i in range(size):
    input_map[i] = list(input())

start_time = time()

class Drone:
    def __init__(self):
        
        self.batt = BATTERY
        self.all_path = ''
        self.path = ''
        self.coords = [0, 0]
        count_last[0][0] += 1

    def move(self, coords, dir):
        self.all_path += dir
        self.path += dir
        
        self.batt -= 1
        self.coords = coords
        
        count_last[self.coords[0]][self.coords[1]] += 1

        if self.coords == [0, 0]:
            self.batt = BATTERY

    def return_to_base(self):
        last_move = self.path[-1]

        rev_dir = reverse(last_move)

        self.all_path += rev_dir
        self.path = self.path[:len(self.path) - 1]
        
        self.batt -= 1
        self.coords = calc_coords(self.coords, rev_dir)
        
        count_last[self.coords[0]][self.coords[1]] += 1

        if self.coords == [0, 0]:
            self.batt = BATTERY


def calc_coords(coords, dir):
    if dir == 'U':
        coords[0] -= 1
    elif dir == 'D':
        coords[0] += 1
    elif dir == 'L':
        coords[1] -= 1
    elif dir == 'R':
        coords[1] += 1
    elif dir == 'I':
        pass
    return coords


def reverse(dir):
    if dir == 'U':
        return 'D'
    elif dir == 'D':
        return 'U'
    elif dir == 'L':
        return 'R'
    elif dir == 'R':
        return 'L'
    return 'I'


def findDirection(drone):
    cur_coords = (drone.coords[0], drone.coords[1])
    variants = neighbours[cur_coords]
    dir = min(variants, key=lambda x: count_last[x[0]][x[1]])

    return dir

neighbours = {}
count_last = numpy.zeros([size, size], dtype=int)

directions = {(-1, 0): 'U',
              (0, 1): 'R',
              (1, 0): 'D',
              (0, -1): 'L'}

for i in range(size):
    for j in range(size):
        if input_map[i][j] != '.':
            for dir in directions:
                if 0 <= i + dir[0] < size and 0 <= j + dir[1] < size:
                    if input_map[i + dir[0]][j + dir[1]] != '.':
                        if (i, j) not in neighbours:                                                
                            neighbours[(i, j)] = [(i + dir[0], j + dir[1], directions[dir])]
                        else:
                            neighbours[(i, j)].append((i + dir[0], j + dir[1], directions[dir]))
        else:
            count_last[i][j] = -1

num_drones = math.ceil(len(neighbours) // (BATTERY // 2))**2

drones = [Drone() for i in range(num_drones)]
for i in range(STEPS):
    for drone in drones:
        if drone.batt > BATTERY // 2:  # +1?
            dir = findDirection(drone)
            drone.move([dir[0], dir[1]], dir[2])
        else:
            drone.return_to_base()

# print(drones[0].all_path)
# print(map)

print(num_drones)
for i in range(STEPS):
    for drone in drones:
        print(drone.all_path[i], end='')
    print()