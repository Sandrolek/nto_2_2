from itertools import permutations
import math

memo = {}


def dist(a, b):
    memo_key = (abs(a[0] - b[0]), abs(a[1] - b[1]))
    if memo_key not in memo:
        memo[memo_key] = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    return memo[memo_key]


def prem_to_nodes(prem):
    return [nodes[p] for p in prem]


def path_len(prem):
    l = 0
    t = prem_to_nodes(prem)
    for a, b in zip([start] + t, t + [end]):
        l += dist(a, b)
    return l


# input
start = tuple(map(int, input().split()))
end = tuple(map(int, input().split()))
nodes = []
inp = "0 0 0"
inp = input().split()
while len(inp) == 3:
    nodes.append(inp)
    inp = input().split()
nodes = list(map(lambda x: tuple(map(int, x[1:])), filter(lambda x: x[0] == inp[0], nodes)))

# solution
prems = [p for p in permutations(range(len(nodes)))]
min_prem = min(prems, key=path_len)
#print([start] + prem_to_nodes(min_prem) + [end])

for i in prem_to_nodes(min_prem):
    print(f"navigate(x={i[0]}, y={i[1]})")
