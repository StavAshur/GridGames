from random import randrange, choice
from copy import deepcopy
import networkx as nx
from time import sleep

def convert_grid(g, width = None, height = None):
    if not width:
        width = 0
        for node in g.nodes:
            if node[0]+1 > width:
                width = node[0]+1
    if not height:
        height = 0
        for node in g.nodes:
            if node[1]+1 > height:
                height = node[1]+1
    grid = [[None for j in range(width)] for i in range(height)]
    for node in g.nodes:
        grid[node[1]][node[0]] = node
    return grid

def holes(g):
    g = convert_grid(g)
    #patched = nx.grid_2d_graph(len(g), len(g[0]))
    output = []
    [[output.append(((j, i))) if not g[i][j] else None for j in range(len(g[i]))] for i in range(len(g))]
    return output

def print_grid(g, specials = {}):
    g = convert_grid(g)
    for i in range(len(g)):
        row = g[i]
        for j in range(len(row)):
            cell = row[j]
            char = "⬜" if cell else "⬛"
            for pos in specials.keys():
                if i == pos[1] and j == pos[0]:
                    char = specials[pos]
            print(char, end="")
        print()

def neighborhood(pos, size = 1):
    output = []
    [[output.append((pos[0]+i, pos[1]+j)) for j in range(-size, size+1)] for i in range(-size, size+1)]
    return output

def main():
    size = 50
    wallChance = 30
    #Actual agent width is twice this plus one
    agentSize = 2
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
    [g.remove_node(node) if node in walls else None for node in nodes]
    nodes = [node for node in g.nodes.keys()]
    agent = choice(nodes)
    targets = neighborhood(ball, agentSize+1)
    #print_grid(g, {ball:"🟥", agent:"🟦"})
    #print(ball)
       
    target = ball
    while target not in g.nodes:
        try:
            target = targets.pop()
        except IndexError:
            ball = choice(list(display_grid.nodes.keys()))
            targets = neighborhood(ball, agentSize+1)
            target = ball
            
    try:
        while True:
            print()
            agent = nx.shortest_path(g, agent, target)[1]
            display_specials = {ball:"🟥"}
            [display_specials.update({pos: "🟦"}) for pos in neighborhood(agent, agentSize)]
            """print_grid(display_grid, {
                ball:"🟥", 
                agent:"🟦",
                (agent[0]+1, agent[1]+1):"🟦",
                (agent[0]-1, agent[1]+1):"🟦",
                (agent[0], agent[1]+1):"🟦",
                (agent[0]+1, agent[1]-1):"🟦",
                (agent[0]-1, agent[1]-1):"🟦",
                (agent[0], agent[1]-1):"🟦",
                (agent[0]+1, agent[1]):"🟦",
                (agent[0]-1, agent[1]):"🟦",
                })"""
            print_grid(display_grid, display_specials)
            sleep(0.01)
    except IndexError:
        pass
    except nx.NetworkXNoPath:
        print("nx.NetworkXNoPath")
        main()


    

if __name__ == "__main__":
    main()