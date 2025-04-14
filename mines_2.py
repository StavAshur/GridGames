from random import random, choice
from copy import copy, deepcopy
import networkx as nx
from time import sleep
import sys
import maze

def add_edge_to_graph(g, node1, node2, weight = 1, nodeNotFoundMode = None):
    match nodeNotFoundMode:
        case "error":
            if not(g.has_node(node1) and g.has_node(node2)):
                raise nx.NodeNotFound
            g.add_edge(node1, node2)
            g[node1][node2]["weight"] = weight
        case "add":
            if not g.has_node(node1): g.add_node(node1)
            if not g.has_node(node2): g.add_node(node2)
            g.add_edge(node1, node2)
            g[node1][node2]["weight"] = weight
        case _:
            if(g.has_node(node1) and g.has_node(node2)):
                g.add_edge(node1, node2)
                g[node1][node2]["weight"] = weight

def convert_grid(g, width = None, height = None):
    if not width:
        width = sorted([node for node in g.nodes.keys()], key = lambda x: x[0])[-1][0] + 1
    if not height:
        height= sorted([node for node in g.nodes.keys()], key = lambda x: x[1])[-1][1] + 1
    grid = [[None for j in range(width)] for i in range(height)]
    for node in g.nodes:
        try:
            grid[node[1]][node[0]] = node
        except IndexError:
            pass
    return grid

def holes(g, width = None, height = None):
    g = convert_grid(g, width, height)
    output = []
    [[output.append(((j, i))) if not g[i][j] else None for j in range(len(g[i]))] for i in range(len(g))]
    return output

def print_grid(g, specials = {}, width = None, height = None):
    output = ""
    g = convert_grid(g, width, height)
    for i in range(len(g)):
        row = g[i]
        for j in range(len(row)):
            cell = row[j]
            char = "⬜" if cell else "⬛"
            for pos in specials.keys():
                if i == pos[1] and j == pos[0]:
                    char = specials[pos]
            output = output + char
        output = f"{output}\n"
    print(output)
    return output

def neighborhood(pos, size = 1, include_original = False):
    output = []
    [[output.append((pos[0]+i, pos[1]+j)) for j in range(-size, size+1)] for i in range(-size, size+1)]
    if not include_original:
        output.remove(pos)
    return output

def adjacent(pos):
    return [(pos[0], pos[1]+1), (pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]-1)]

def shortest_path_between_sets(g, set1, set2):
    g2 = nx.Graph()
    [g2.add_node(node) for node in g if not(node in set1.union(set2))]
    [add_edge_to_graph(g2, edge[0], edge[1]) for edge in g.edges()]
    print_grid(g2)
    n1 = "/"
    n2 = "\\"
    g2.add_node(n1)
    g2.add_node(n2)
    [add_edge_to_graph(g2, n1, edge[1]) for edge in g.edges() if edge[0] in set1]
    [add_edge_to_graph(g2, n2, edge[1]) for edge in g.edges() if edge[0] in set2]
    output = nx.shortest_path(g2, n1, n2)
    output.remove(n1)
    output.remove(n2)
    return output

def check_sets(edge, s1, s2):
    return (edge[0] in s1 and edge[1] not in s2) or (edge[1] in s1 and edge[0] not in s2)
"""
def idontknowwhattocallthis(g, g2, s1, u):
    for edge in g.edges:
        if check_sets(edge, s1, u):
            add_edge_to_graph(g2, ) if edge[0]
"""
def shortest_path_between_many_sets(g, sets, start, end, start_node=None, end_node=None):
    if not(start in sets and end in sets):
        raise ValueError("Start and end are not in provided sets!")
    if start == end:
        raise ValueError("Start is end!")
    if start_node and end_node and not(end_node in end and start_node in start):
        raise ValueError("Start and end nodes must either be in start and end sets respectively or NoneType")
    u = sets[0]
    for s in sets:
        u = u.union(s) 
    g2 = nx.Graph()
    [g2.add_node(node) for node in g if not(node in u)]
    [add_edge_to_graph(g2, edge[0], edge[1]) for edge in g.edges()]
    #print_grid(g2)
    sets.remove(start)
    sets.remove(end)
    n1 = "/"
    n2 = "\\"
    g2.add_node(n1)
    g2.add_node(n2)
    [g2.add_edge(n1, edge[1])if edge[0] in start else g2.add_edge(n1, edge[0]) for edge in g.edges if check_sets(edge, start, u)]
    [g2.add_edge(n2, edge[1])if edge[0] in end else g2.add_edge(n2, edge[0]) for edge in g.edges if check_sets(edge, end, u)]
    for i in range(len(sets)):
        g2.add_node(i)
        [g2.add_edge(i, edge[1]) if edge[0] in sets[i] else g2.add_edge(i, edge[0]) for edge in g.edges if check_sets(edge, sets[i], u)]
    #print(g2.edges())
    [add_edge_to_graph(g2, edge[0], edge[1]) for edge in g.edges() if edge[1] not in u and edge[0] not in u]
    #print("HELLO?")
    #print([node for node in g2 if node not in nx.bfs_tree(g2, n1).nodes])
    #print(nx.bfs_tree(g2, n1))
    #print([node for node in g2 if node in nx.bfs_tree(g2, n2).nodes])
    #print(nx.bfs_tree(g2, n2))
    #print()
    path = nx.shortest_path(g2, n1, n2)
    [path.remove(node) for node in path if type(node) == int or node == n1 or node == n2]
    if start_node:
        path.insert(0, start_node)
    if end_node:
        path.append(end_node)

    g3 = nx.Graph()
    [g3.add_node(node) for node in g if node in path or node in u]
    [g3.add_edge(edge[0], edge[1]) for edge in g.edges if (edge[0] in u or edge[0] in path) and (edge[1] in u or edge[1] in path)]
    output = []
    #print(path)
    #print_grid(g3)
    for i in range(len(path)-1):
        output = output + nx.shortest_path(g3, path[i], path[i+1])
    temp = []
    [temp.append(node) for node in output if node not in temp]
    output = temp
    return output


def separate_paths(g, start, end, max_branches = 10, dont = []):
    g = deepcopy(g)
    paths = []
    for i in range(max_branches):
        path = nx.shortest_path(g, start, end, "weight")
        if path not in paths and path not in dont:
            paths.append(path)
        for node in paths[-1]:
            for neighbor in g.neighbors(node):
                g[node][neighbor]["weight"]=len(g.nodes)
    return sorted(paths, key=lambda x:len(x))

def method1():
    size = 10
    wallChance = 50
    mineChance = 2
    start = (0, 0)
    agent = start
    target = (size-1, size-1)
    """g = nx.Graph()
    #Generate wall positions
    [[g.add_node((i, j, True)) if randrange(wallChance) < 1 else g.add_node((i, j, False)) for j in range(size)] for i in range(size)]
    #Remove wall nodes then copy back to original
    g2 = nx.grid_2d_graph(size, size)
    [g2.remove_node((n[0], n[1])) for n in g if n[2]]
    g = g2
    g.add_nodes_from((agent, target))
    #Generate mine positions
    mines = [node for node in g if randrange(mineChance) < 1]
    try:
        for node1 in g.nodes:
            for node2 in adjacent(node1):
                if node1 in g.nodes and node2 in g.nodes and node1 not in mines and node2 not in mines:
                    g[node1][node2]['weight'] = 0
    except KeyError:
        main()"""
    g = maze.generate_maze(size, agent, target)
    mines = []
    for node in holes(g):
        g.add_node(node)
        add_edge_to_graph(g, node, (node[0]-1, node[1]),weight=size*size)
        add_edge_to_graph(g, node, (node[0]+1, node[1]),weight=size*size)
        add_edge_to_graph(g, node, (node[0], node[1]-1),weight=size*size)
        add_edge_to_graph(g, node, (node[0], node[1]+1),weight=size*size)
        mines.append(node)
        
    try:
        path = nx.shortest_path(g, agent, target, weight="weight")
        for node in path:
            agent = node
            display_specials = {agent:"🟦", target:"🟩"}
            [display_specials.update({pos: "🟥"}) for pos in mines]
            [display_specials.update({pos: "🟩"}) for pos in path[path.index(node): len(path)-1]]
            display_specials.update({agent:"🟦", target:"🟥"})
            print_grid(g, display_specials)
            #sleep(0.01)
        sys.exit()
    except IndexError:
        pass
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        method1()

def mines_in_path(path, mines):
    return [node for node in path if node in mines]

def method2():
    size = 50
    wallChance = 10
    mineChance = 2
    start = (0, 0)
    agent = start
    target = (size-1, size-1)
    max_mines = 10

    g = nx.Graph()
    #Generate wall positions
    [[g.add_node((i, j, True)) if random()*wallChance < 1 else g.add_node((i, j, False)) for j in range(size)] for i in range(size)]
    #Remove wall nodes then copy back to original
    g2 = nx.grid_2d_graph(size, size)
    [g2.remove_node((n[0], n[1])) for n in g if n[2]]
    g = deepcopy(g2)
    g.add_nodes_from((agent, target))
    #Generate mine positions
    mines = [node for node in g if random()*mineChance < 1 and node != agent and node != target]
    #mines = [(0, 1), (0,2), (1, 1), (1, 2), (2,0)]
    
    g2 = nx.Graph()
    [g2.add_node(node) for node in g if not(node in mines)]
    [add_edge_to_graph(g2, edge[0], edge[1]) for edge in g.edges()]
    display_specials = {agent:"🟦", target:"🟩"}
    [display_specials.update({pos: "🟥"}) for pos in mines]        
    print_grid(g, display_specials)
    try:
        #path = shortest_path_between_sets(g, set(nx.bfs_tree(g2, agent)), set(nx.bfs_tree(g2, target)))
        path = shortest_path_between_many_sets(
            g, 
            list(nx.connected_components(g2)), 
            set(nx.bfs_tree(g2, agent)), 
            set(nx.bfs_tree(g2, target)),
            agent, target
            )
    except NameError:
        method2()
    print(path)
    #sys.exit()

    """steps = 0
    max_steps = 50
    try:
        path = nx.shortest_path(g, agent, target)
    except nx.NetworkXNoPath:
        print("No path")
        method2()
    dont = []
    print("Testing paths...")
    while len(mines_in_path(path, mines)) > max_mines and steps < max_steps:
        steps += 1
        paths = sorted(separate_paths(g, agent, target), key = lambda x: mines_in_path(x, mines))
        if len(mines_in_path(path, mines)) > len(mines_in_path(paths[0], mines)):
            path = paths[0]
        dont += paths
    if(steps == max_steps):
        print("FAILURE")
        print(path)
        print("Landmines touched:", mines_in_path(path, mines))
        print(len(mines_in_path(path, mines)), "mines total")
        display_specials = {}
        [display_specials.update({pos: "🟥"}) for pos in mines]
        [display_specials.update({pos: "🟢"}) for pos in mines_in_path(path, mines)]
        print_grid(g, display_specials)
        sys.exit()"""

    try:
        for node in path:
            agent = node
            display_specials = {agent:"🟦", target:"🟩"}
            [display_specials.update({pos: "🟥"}) for pos in mines]
            [display_specials.update({pos: "🟩"}) for pos in path[path.index(node): len(path)-1]]
            [display_specials.update({pos: "🟡"}) for pos in mines_in_path(path, mines)]
            display_specials.update({agent:"🟦", target:"🟩"})
            print_grid(g, display_specials)
            #sleep(0.01)
        #Display full path at end
        display_specials = {agent:"🟦", target:"🟩"}
        [display_specials.update({pos: "🟥"}) for pos in mines]
        [display_specials.update({pos: "🟩"}) for pos in path[: len(path)-1]]
        [display_specials.update({pos: "🟡"}) for pos in mines_in_path(path, mines)]
        display_specials.update({start:"🟦", target:"🟩"})
        print_grid(g, display_specials)
        print(len(mines_in_path(path, mines)), "Unplanned explosions")
            
        sys.exit()
    except IndexError:
        pass
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        method2()


if __name__ == "__main__":
    #method1()
    method2()
















"""
    g2 = deepcopy(g)
    for node in deepcopy(g2.nodes):
        g2.add_node((node[0], node[1], 0))
        g2.remove_node(node)
    for node in g2.nodes:
        add_edge_to_graph(g2, node, (node[0]-1, node[1], node[2]))
        add_edge_to_graph(g2, node, (node[0]+1, node[1], node[2]))
        add_edge_to_graph(g2, node, (node[0], node[1]-1, node[2]))
        add_edge_to_graph(g2, node, (node[0], node[1]+1, node[2]))
    print(g2.nodes)
    for node in sorted(g2.nodes, key = lambda x: abs(x[0]-agent[0]) + abs(x[1]-agent[1])):
        nodecopy = copy(node)
        try:
            print([node2[2] for node2 in g2.neighbors(node) if node2[0] <= node[0] and node2[1] <= node[1]])
            node = (node[0], node[1], min([node2[2] for node2 in g2.neighbors(node) if node2[0] <= node[0] and node2[1] <= node[1]]))
        except ValueError:
            print("ValueError", end="")
        if (node[0], node[1]) in mines:
            node = (node[0], node[1], node[2] + 1)
        g2.add_node(node)
        [g2.add_edge(node, node2) for node2 in g2.neighbors(nodecopy)]"""