from random import randrange, choice
from copy import deepcopy
import networkx as nx
from time import sleep
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

def neighborhood(pos, size = 1, include_original = False):
    output = []
    [[output.append((pos[0]+i, pos[1]+j)) for j in range(-size, size+1)] for i in range(-size, size+1)]
    if not include_original:
        output.remove(pos)
    return output

def main():
    size = 50
    wallChance = 10
    #Actual agent width is twice this plus one
    agentSize = 1
    g = nx.Graph()
    [[g.add_node((i, j, False)) if randrange(wallChance) < 1 else g.add_node((i, j, True)) for j in range(size)] for i in range(size)]
    g2 = nx.grid_2d_graph(size, size)
    [g2.remove_node((n[0], n[1])) if not n[2] else None for n in g]
    g = g2

    walls = [(0, i)for i in range(size)]+[(i, 0)for i in range(size)]+[(size-1, i)for i in range(size)]+[(i, size-1)for i in range(size)]
    for hole in holes(g):
        width = len(convert_grid(g)[0])
        height= len(convert_grid(g))
        """
        if(hole[1]+1 < height):
            walls.append((hole[0]-1, hole[1]+1))
            walls.append((hole[0]+1, hole[1]+1))
            walls.append((hole[0], hole[1]+1))
        if(hole[1]-1 > -1):
            walls.append((hole[0]-1, hole[1]-1))
            walls.append((hole[0]+1, hole[1]-1))
            walls.append((hole[0], hole[1]-1))
        walls.append((hole[0]-1, hole[1]))
        walls.append((hole[0]+1, hole[1]))
        """
        [walls.append(wall) if(-1 < wall[0] < width and -1 < wall[1] < height) else None for wall in neighborhood(hole, agentSize)]
    
    display_grid = deepcopy(g)
    nodes = [node for node in g.nodes.keys()]
    ball = choice(nodes)
    dropoff = choice(nodes)
    [g.remove_node(node) if node in walls else None for node in nodes]
    nodes = [node for node in g.nodes.keys()]
    agent = choice(nodes)
    targets = neighborhood(ball, agentSize+1)
    #print_grid(g, {ball:"🟥", agent:"🟦"})
    #print(ball)

    #Ensure path between dropoff and start exists
    target = dropoff
    targets=[dropoff, (dropoff[0]-2, dropoff[1]), (dropoff[0]+2, dropoff[1]), (dropoff[0], dropoff[1]+2), (dropoff[0], dropoff[1]-2)]
    while target not in g.nodes:
        try:
            target = targets.pop()
        except IndexError:
            dropoff = choice(list(display_grid.nodes.keys()))
            targets = neighborhood(dropoff, agentSize+1)
            target = dropoff
    try:
        nx.shortest_path(g, agent, target)
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        main()

    #Ensure path between start and ball exists
    target = ball
    targets = neighborhood(ball, agentSize+1)
    while target not in g.nodes:
        try:
            target = targets.pop()
        except IndexError:
            ball = choice(list(display_grid.nodes.keys()))
            targets = neighborhood(ball, agentSize+1)
            target = ball
    try:
        nx.shortest_path(g, agent, target)
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        main()
    print("Sucess")
            
    try:
        path = nx.shortest_path(g, agent, target)
        for node in path:
            #agent = nx.shortest_path(g, agent, target)[1]
            agent = node
            display_specials = {dropoff:"🟦", ball:"🟥"}
            [display_specials.update({pos: "🟨"}) for pos in nx.bfs_tree(g, agent)]
            [display_specials.update({pos: "🟩"}) for pos in path[path.index(node): len(path)-1]]
            [display_specials.update({pos: "🟦"}) for pos in neighborhood(agent, agentSize, True)]
            display_specials.update({dropoff:"🟦", ball:"🟥"})
            #print()
            print_grid(display_grid, display_specials)
            sleep(0.01)
        target = dropoff
        targets=[(dropoff[0]-2, dropoff[1]), (dropoff[0]+2, dropoff[1]), (dropoff[0], dropoff[1]+2), (dropoff[0], dropoff[1]-2)]
        while target not in g.nodes:
            try:
                target = targets.pop()
            except IndexError:
                dropoff = choice(list(display_grid.nodes.keys()))
                targets=[(dropoff[0]-2, dropoff[1]),(dropoff[0]+2, dropoff[1]),(dropoff[0], dropoff[1]+2),(dropoff[0], dropoff[1]-2)]
                target = dropoff
        path = nx.shortest_path(g, agent, target)
        for node in path:
            #agent = nx.shortest_path(g, agent, target)[1]
            agent = node
            ball = agent
            display_specials = {dropoff:"🟦", ball:"🟥"}
            [display_specials.update({pos: "🟨"}) for pos in nx.bfs_tree(g, agent)]
            [display_specials.update({pos: "🟩"}) for pos in path[path.index(node): len(path)-1]]
            [display_specials.update({pos: "🟦"}) for pos in neighborhood(agent, agentSize, True)]
            display_specials.update({dropoff:"🟦", ball:"🟥"})
            #print()
            print_grid(display_grid, display_specials)
            sleep(0.01)
        ball = dropoff
        display_specials = {dropoff:"🟦", ball:"🟥"}
        [display_specials.update({pos: "🟨"}) for pos in nx.bfs_tree(g, agent)]
        [display_specials.update({pos: "🟩"}) for pos in path[path.index(node): len(path)-1]]
        [display_specials.update({pos: "🟦"}) for pos in neighborhood(agent, agentSize, True)]
        display_specials.update({dropoff:"🟦", ball:"🟥"})
        print_grid(display_grid, display_specials)
        sys.exit()
    except IndexError:
        pass
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        main()    

if __name__ == "__main__":
    main()