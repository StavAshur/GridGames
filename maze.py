import networkx as nx
import random
import time
import sys

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
    if(type(g) == int):
        size = g
        g = nx.grid_2d_graph(size, size)
    elif(type(g) == float):
        size = round(g)
        g = nx.grid_2d_graph(size, size)
    elif(type(g) == nx.graph):
        size = len(convert_grid(g))
    
    if (not steps) or steps <= 0:
        steps = int(len(g)/2)
    
    for _ in range(steps):
        node = random.choice([node for node in g.nodes.keys()])
        path = []
        if node not in [start, end]:
            g.remove_node(node)
        try:
            path = nx.shortest_path(g, start, end)
        except nx.NetworkXNoPath:
            h = holes(g, size, size)
            g.add_node(node)
            add_edge_to_graph(g, node, (node[0]-1, node[1]))
            add_edge_to_graph(g, node, (node[0]+1, node[1]))
            add_edge_to_graph(g, node, (node[0], node[1]-1))
            add_edge_to_graph(g, node, (node[0], node[1]+1))
            node = random.choice(h)
            g.add_node(node)
            add_edge_to_graph(g, node, (node[0]-1, node[1]))
            add_edge_to_graph(g, node, (node[0]+1, node[1]))
            add_edge_to_graph(g, node, (node[0], node[1]-1))
            add_edge_to_graph(g, node, (node[0], node[1]+1))
            node = random.choice(h)
            g.add_node(node)
            add_edge_to_graph(g, node, (node[0]-1, node[1]))
            add_edge_to_graph(g, node, (node[0]+1, node[1]))
            add_edge_to_graph(g, node, (node[0], node[1]-1))
            add_edge_to_graph(g, node, (node[0], node[1]+1))
        if watch:
            specials = {start: "🟦", end: "🟥"}
            if path: [specials.update({node: "🟩"}) for node in path]
            #Ensure they render in front
            specials.update({start: "🟦", end: "🟥"})
            print_grid(g, specials)
            print()
            time.sleep(0.01)
    return g

def connect_components(g, components = None):
    if not components:
        components = nx.connected_components(g)
    fake_grid = nx.grid_2d_graph(len(convert_grid(g)[0]), len(convert_grid(g)))
    for i in range(len(components)):
        for node in holes(g):
            if (True in [neighbor in components[0] for neighbor in neighborhood(node)]) and (
                True in [neighbor in components[i] for neighbor in neighborhood(node)]):
                g.add_node(node)
                add_edge_to_graph(g, node, (node[0]-1, node[1]))
                add_edge_to_graph(g, node, (node[0]+1, node[1]))
                add_edge_to_graph(g, node, (node[0], node[1]-1))
                add_edge_to_graph(g, node, (node[0], node[1]+1))
                break
    for i in range(len(components)):
        for node in holes(g):
            if (True in [neighbor in components[0] for neighbor in neighborhood(node)]) and (
                True in [neighbor in components[i] for neighbor in neighborhood(node)]):
                g.add_node(node)
                add_edge_to_graph(g, node, (node[0]-1, node[1]))
                add_edge_to_graph(g, node, (node[0]+1, node[1]))
                add_edge_to_graph(g, node, (node[0], node[1]-1))
                add_edge_to_graph(g, node, (node[0], node[1]+1))
                break
    return g

def display(g, start, end):
    specials = {start: "🟦", end: "🟥"}
    [specials.update({node: "🟩"}) for node in nx.shortest_path(g, start, end)]
    print_grid(g, specials)
    print()
    print()
    components = list(nx.connected_components(g))
    print(len(components))
    colors = list("🟧🟨🟪🟫🔴🟠🟡🟢🔵🟣✅")
    components = [tree for tree in components if not len(set(nx.bfs_tree(g, start)).difference(set(tree))) < 1]
    components = sorted(components, reverse=True, key=lambda x:len(x))[:len(colors)]
    [[specials.update({node: colors[i]}) for node in components[i]] for i in range(len(components))]
    [specials.update({node: "🟩"}) for node in nx.bfs_tree(g, start)]
    print_grid(g, specials)
    print()
    print()
    print_grid(g, {start: "🟦", end: "🟥"})

def main():
    size = 50
    g = nx.grid_2d_graph(size, size)
    start = (0, 0)
    end = (size-1, size-1)
    g = generate_maze(g, start, end, watch = not "-t" in sys.argv)
    for _ in range(3):
        intermediate = random.choice([node for node in g.nodes.keys() if node not in nx.bfs_tree(g, start)])
        g = generate_maze(g, start, intermediate, 1, not "-t" in sys.argv )
    """specials = {start: "🟦", end: "🟥"}
    [specials.update({node: "🟩"}) for node in nx.shortest_path(g, start, end)]
    print_grid(g, specials)
    print()
    print()
    components = list(nx.connected_components(g))
    print(len(components))
    colors = list("🟧🟨🟪🟫🔴🟠🟡🟢🔵🟣✅")
    components = [tree for tree in components if not len(set(nx.bfs_tree(g, start)).difference(set(tree))) < 1]
    components = sorted(components, reverse=True, key=lambda x:len(x))[:len(colors)]
    [[specials.update({node: colors[i]}) for node in components[i]] for i in range(len(components))]
    [specials.update({node: "🟩"}) for node in nx.bfs_tree(g, start)]
    print_grid(g, specials)
    print()
    print()
    print_grid(g, {start: "🟦", end: "🟥"})"""
    display(g, start, end)
    components = list(nx.connected_components(g))
    components = sorted(components, reverse=True, key=lambda x:len(x))#[:10]
    g = connect_components(g, components)
    display(g, start, end)
    
if __name__ == "__main__":
    main()