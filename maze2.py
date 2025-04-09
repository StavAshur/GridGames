import networkx as nx
import random
import time
import sys
import maze

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

def add_edge_to_graph(g, node1, node2, nodeNotFoundMode = None):
    match nodeNotFoundMode:
        case "error":
            if not(g.has_node(node1) and g.has_node(node2)):
                raise nx.NodeNotFound
            g.add_edge(node1, node2)
        case "add":
            if not g.has_node(node1): g.add_node(node1)
            if not g.has_node(node2): g.add_node(node2)
            g.add_edge(node1, node2)
        case _:
            if(g.has_node(node1) and g.has_node(node2)):
                g.add_edge(node1, node2)

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
            #print(char, end="")
            output = output + char
        output = f"{output}\n"
    print(output)
    return output

def neighborhood(pos, size = 1):
    output = []
    [[output.append((pos[0]+i, pos[1]+j)) for j in range(-size, size+1)] for i in range(-size, size+1)]
    return output

def generate_maze(g, start, end, steps = None, watch = False):
    size = 20
    g2 = None
    if(type(g) == int):
        size = g
        g = maze.generate_maze(size, start, end, steps, watch)
        g2 = nx.grid_2d_graph(size, size)
    elif(type(g) == float):
        size = round(g)
        g = maze.generate_maze(size, start, end, steps, watch)
        g2 = nx.grid_2d_graph(size, size)
    elif(type(g) == nx.graph):
        size = len(convert_grid(g))
        g2 = nx.grid_2d_graph(size, size)
    
    if (not steps) or steps <= 0:
        steps = int(size/2)
    
    steps = [start]+[random.choice(list((g2.nodes.keys()))) for _ in range(steps)]+[end]
    for i in range(len(steps)-1):
        #path = nx.shortest_path(g2, random.choice(list(g.nodes.keys())), random.choice(list(g.nodes.keys())))
        path = nx.shortest_path(g2, steps[i], steps[i+1])
        [g.add_node(node) for node in path]
        if watch:
            specials = {start: "🟦", end: "🟥"}
            [specials.update({node: "🟩"}) for node in path]
            #Ensure they render in front
            specials.update({start: "🟦", end: "🟥"})
            print_grid(g, specials)
            print()
            time.sleep(0.01)
    print_grid(g)
    return g

size = 50
generate_maze(size, (0, 0), (size-1, size-1), watch=True)