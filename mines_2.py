from random import randrange, choice
from copy import deepcopy
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

def method1():
    size = 50
    wallChance = 10
    mineChance = 20
    agent = (0, 0)
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
            display_specials = {agent:"🟦", target:"🟥"}
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



if __name__ == "__main__":
    method1()