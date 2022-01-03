import math
import networkx as nx
from networkx.utils import py_random_state, not_implemented_for, pairwise

__all__ = [
    "traveling_salesman_problem",
    "christofides",
    "greedy_tsp",
    "simulated_annealing_tsp",
    "threshold_accepting_tsp",
]


def swap_two_nodes(soln, seed):
    a, b = seed.sample(range(1, len(soln) - 1), k=2)
    soln[a], soln[b] = soln[b], soln[a]
    return soln


def move_one_node(soln, seed):
    a, b = seed.sample(range(1, len(soln) - 1), k=2)
    soln.insert(b, soln.pop(a))
    return soln

def christofides(G, weight="weight", tree=None):
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)
    # Check that G is a complete graph
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    if tree is None:
        tree = nx.minimum_spanning_tree(G, weight=weight)
    L = G.copy()
    L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])
    MG = nx.MultiGraph()
    MG.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, maxcardinality=True, weight=weight)
    MG.add_edges_from(edges)
    return _shortcutting(nx.eulerian_circuit(MG))



def _shortcutting(circuit):
    """Remove duplicate nodes in the path"""
    nodes = []
    for u, v in circuit:
        if v in nodes:
            continue
        if not nodes:
            nodes.append(u)
        nodes.append(v)
    nodes.append(nodes[0])
    return nodes


def traveling_salesman_problem(G, weight="weight", nodes=None, cycle=True, method=None):
    if method is None:
        if G.is_directed():

            def threshold_tsp(G, weight):
                return threshold_accepting_tsp(G, "greedy", weight)

            method = threshold_tsp
        else:
            method = christofides
    if nodes is None:
        nodes = list(G.nodes)

    dist = {}
    path = {}
    for n, (d, p) in nx.all_pairs_dijkstra(G, weight=weight):
        dist[n] = d
        path[n] = p

    GG = nx.Graph()
    for u in nodes:
        for v in nodes:
            if u == v:
                continue
            GG.add_edge(u, v, weight=dist[u][v])
    best_GG = method(GG, weight)

    if not cycle:
        # find and remove the biggest edge
        biggest_edge = None
        length_biggest = float("-inf")
        (u, v) = max(pairwise(best_GG), key=lambda x: dist[x[0]][x[1]])
        pos = best_GG.index(u) + 1
        while best_GG[pos] != v:
            pos = best_GG[pos:].index(u) + 1
        best_GG = best_GG[pos:-1] + best_GG[:pos]

    best_path = []
    for u, v in pairwise(best_GG):
        best_path.extend(path[u][v][:-1])
    best_path.append(v)
    return best_path



def greedy_tsp(G, weight="weight", source=None):
    # Check that G is a complete graph
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    if source is None:
        source = nx.utils.arbitrary_element(G)

    if G.number_of_nodes() == 2:
        neighbor = next(G.neighbors(source))
        return [source, neighbor, source]

    nodeset = set(G)
    nodeset.remove(source)
    cycle = [source]
    next_node = source
    while nodeset:
        nbrdict = G[next_node]
        next_node = min(nodeset, key=lambda n: nbrdict[n].get(weight, 1))
        cycle.append(next_node)
        nodeset.remove(next_node)
    cycle.append(cycle[0])
    return cycle

def simulated_annealing_tsp(
    G,
    init_cycle,
    weight="weight",
    source=None,
    temp=100,
    move="1-1",
    max_iterations=10,
    N_inner=100,
    alpha=0.01,
    seed=None,
):
    if move == "1-1":
        move = swap_two_nodes
    elif move == "1-0":
        move = move_one_node
    if init_cycle == "greedy":
        # Construct an initial solution using a greedy algorithm.
        cycle = greedy_tsp(G, weight=weight, source=source)
        if G.number_of_nodes() == 2:
            return cycle

    else:
        cycle = list(init_cycle)
        if source is None:
            source = cycle[0]
        elif source != cycle[0]:
            raise nx.NetworkXError("source must be first node in init_cycle")
        if cycle[0] != cycle[-1]:
            raise nx.NetworkXError("init_cycle must be a cycle. (return to start)")

        if len(cycle) - 1 != len(G) or len(set(G.nbunch_iter(cycle))) != len(G):
            raise nx.NetworkXError("init_cycle should be a cycle over all nodes in G.")

        # Check that G is a complete graph
        N = len(G) - 1
        # This check ignores selfloops which is what we want here.
        if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in G.adj.items()):
            raise nx.NetworkXError("G must be a complete graph.")

        if G.number_of_nodes() == 2:
            neighbor = next(G.neighbors(source))
            return [source, neighbor, source]

    # Find the cost of initial solution
    cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(cycle))

    count = 0
    best_cycle = cycle.copy()
    best_cost = cost
    while count <= max_iterations and temp > 0:
        count += 1
        for i in range(N_inner):
            adj_sol = move(cycle, seed)
            adj_cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(adj_sol))
            delta = adj_cost - cost
            if delta <= 0:
                # Set current solution the adjacent solution.
                cycle = adj_sol
                cost = adj_cost

                if cost < best_cost:
                    count = 0
                    best_cycle = cycle.copy()
                    best_cost = cost
            else:
                # Accept even a worse solution with probability p.
                p = math.exp(-delta / temp)
                if p >= seed.random():
                    cycle = adj_sol
                    cost = adj_cost
        temp -= temp * alpha

    return best_cycle

def threshold_accepting_tsp(
    G,
    init_cycle,
    weight="weight",
    source=None,
    threshold=1,
    move="1-1",
    max_iterations=10,
    N_inner=100,
    alpha=0.1,
    seed=None,
):
    if move == "1-1":
        move = swap_two_nodes
    elif move == "1-0":
        move = move_one_node
    if init_cycle == "greedy":
        # Construct an initial solution using a greedy algorithm.
        cycle = greedy_tsp(G, weight=weight, source=source)
        if G.number_of_nodes() == 2:
            return cycle

    else:
        cycle = list(init_cycle)
        if source is None:
            source = cycle[0]
        elif source != cycle[0]:
            raise nx.NetworkXError("source must be first node in init_cycle")
        if cycle[0] != cycle[-1]:
            raise nx.NetworkXError("init_cycle must be a cycle. (return to start)")

        if len(cycle) - 1 != len(G) or len(set(G.nbunch_iter(cycle))) != len(G):
            raise nx.NetworkXError("init_cycle is not all and only nodes.")

        # Check that G is a complete graph
        N = len(G) - 1
        # This check ignores selfloops which is what we want here.
        if any(len(nbrdict) - (n in nbrdict) != N for n, nbrdict in G.adj.items()):
            raise nx.NetworkXError("G must be a complete graph.")

        if G.number_of_nodes() == 2:
            neighbor = list(G.neighbors(source))[0]
            return [source, neighbor, source]

    # Find the cost of initial solution
    cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(cycle))

    count = 0
    best_cycle = cycle.copy()
    best_cost = cost
    while count <= max_iterations:
        count += 1
        accepted = False
        for i in range(N_inner):
            adj_sol = move(cycle, seed)
            adj_cost = sum(G[u][v].get(weight, 1) for u, v in pairwise(adj_sol))
            delta = adj_cost - cost
            if delta <= threshold:
                accepted = True

                # Set current solution the adjacent solution.
                cycle = adj_sol
                cost = adj_cost

                if cost < best_cost:
                    count = 0
                    best_cycle = cycle.copy()
                    best_cost = cost
        if accepted:
            threshold -= threshold * alpha

    return best_cycle
