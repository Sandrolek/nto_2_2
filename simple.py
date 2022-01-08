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

class Drone:
    def __init__(self, capacity):
        self.capacity = capacity
        self.battery = capacity
        self.main_path = ''
        self.path = ''
        self.coordinates = [0, 0]
        map[0][0] += 1

    def move(self, coords, dir):
        self.main_path += dir
        self.path += dir
        self.battery -= 1
        self.coordinates = coords
        map[self.coordinates[0]][self.coordinates[1]] += 1

        if self.coordinates == [0, 0]:
            self.battery = self.capacity

    def goBack(self):
        last_s = self.path[-1]
        rev_dir = reverse(last_s)

        self.main_path += rev_dir
        self.path = self.path[:len(self.path) - 1]
        self.battery -= 1
        self.coordinates = calcCoords(self.coordinates, rev_dir)
        map[self.coordinates[0]][self.coordinates[1]] += 1

        if self.coordinates == [0, 0]:
            self.battery = self.capacity


def calcCoords(curCoords, dir):
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


def reverse(step):
    if step == 'U':
        return 'D'
    elif step == 'D':
        return 'U'
    elif step == 'L':
        return 'R'
    elif step == 'R':
        return 'L'
    return 'I'


def findDirection(drone):
    cur_coords = (drone.coordinates[0], drone.coordinates[1])
    variants = dict_map[cur_coords]
    dir = min(variants, key=lambda x: map[x[0]][x[1]])

    return dir
    # print(dir)


steps, battery, cost = 0, 0, 0  # inputs
raw_map = []
# n = int(input())
for i in range(int(input())):
    s = input()
    if i == 0:
        steps = int(s)
    elif i == 1:
        battery = int(s)
    elif i == 2:
        cost = int(s)
    else:
        raw_map.append(s)

n = len(raw_map)  # generate map and dict_map
m = len(raw_map[0])
dict_map = {}
map = numpy.zeros([n, m], dtype=int)

directions = {(-1, 0): 'U',
              (0, 1): 'R',
              (1, 0): 'D',
              (0, -1): 'L'}

for i in range(n):
    for j in range(m):
        if raw_map[i][j] != '.':
            for dir in directions:
                if 0 <= i + dir[0] < n and 0 <= j + dir[1] < m:
                    if raw_map[i + dir[0]][j + dir[1]] != '.':
                        if (i, j) not in dict_map:
                            dict_map[(i, j)] = [(i + dir[0], j + dir[1], directions[dir])]
                        else:
                            dict_map[(i, j)].append((i + dir[0], j + dir[1], directions[dir]))
        else:
            map[i][j] = -1

print(map)
print(dict_map)

input()

drone_quantity = math.ceil(len(dict_map) // (battery // 2))**2

print(drone_quantity)
input()

drones = [Drone(battery) for i in range(drone_quantity)]
for i in range(steps):
    for drone in drones:
        if drone.battery > battery // 2:  # +1?
            dir = findDirection(drone)
            drone.move([dir[0], dir[1]], dir[2])
        else:
            drone.goBack()

# print(drones[0].main_path)
# print(map)

print(len(drones))
for i in range(steps):
    for drone in drones:
        print(drone.main_path[i], end='')
    print('')