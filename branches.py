import maze
import networkx as nx
from random import choices
from copy import deepcopy

def separate_paths(g, start, end, max_branches = 10):
    g = deepcopy(g)
    paths = []
    for i in range(max_branches):
        path = nx.shortest_path(g, start, end, "weight")
        if path not in paths:
            paths.append(path) 
        for j in range(len(paths[-1])-1):
            g[paths[-1][j]][paths[-1][j+1]]["weight"] = len(g.nodes)
    return sorted(paths, key=lambda x:len(x))

def separate_paths_2(g, start, end, max_branches = 10):
    g = deepcopy(g)
    paths = []
    for i in range(max_branches):
        path = nx.shortest_path(g, start, end, "weight")
        if path not in paths:
            paths.append(path) 
        for node in paths[-1]:
            for neighbor in g.neighbors(node):
                g[node][neighbor]["weight"]=len(g.nodes)
    return sorted(paths, key=lambda x:len(x))

size = 50
start = (0, 0)
goal = (size-1, size-1)
g = maze.generate_maze(size, start, goal, steps = int(size*size/3))
specials = {}
paths = separate_paths(g, start, goal, 10)
print(len(paths), "branching paths (limit=10)")
colors = list("🟥🟧🟨🟩🟦🟪🟫🔴🟠🟡🟢🔵🟣✅")
[[specials.update({node: colors[i%len(colors)]}) for node in paths[i]] for i in range(len(paths))]
maze.print_grid(g)
maze.print_grid(g, specials)
specials = {}
paths = separate_paths_2(g, start, goal, 10)
print(len(paths), "branching paths (limit=10)")
colors = list("🟥🟧🟨🟩🟦🟪🟫🔴🟠🟡🟢🔵🟣✅")
[[specials.update({node: colors[i%len(colors)]}) for node in paths[i]] for i in range(len(paths))]
maze.print_grid(g, specials)