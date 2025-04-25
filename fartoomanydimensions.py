import networkx as nx
import pygame
import random
import inflect
from math import floor

size = 4
tileSize = 50
numAgents = 3

def contains_duplicates(thelist):
  seen = set()
  for x in thelist:
    if x in seen: return True
    seen.add(x)
  return False

def without(l, e):
    try:
        l.remove(e)
    except:
        return l
    return l

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

def all_possible_combinations(things):
    #This function takes a list of lists (or tuples) and returns all possible combinations that take one thing from each list.
    output = []
    #Similar exec() stuff used to generate the graph, except using the actual things
    string = ""
    inner_string = "("
    p = inflect.engine()
    for i in range(len(things)):
        inner_string += f"{p.number_to_words(i).strip().replace(" ", "_")}, "
    inner_string += ")"
    for i in range(len(things)):
        string = f"""{string}
{"    "*i}for {p.number_to_words(i).strip().replace(" ", "_")} in things[{i}]:"""
    string += f"\n{"    "*len(things)}output.append({inner_string})"
    #print(string)
    l = locals()
    exec(string, globals(), l)
    output = l["output"]
    #print(output)
    #print()
    return output

print(all_possible_combinations([[0, 1], [2, 3]]))

def adjacent(pos):
    return [(pos[0], pos[1]+1), (pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]-1)]

#Note: Each node is a tuple of all agent positions. Yeah.
def all_potential_neighbors(node, size = 1000):
    #output = []
    #This would mean only one could move at a time
    """
    for i in range(len(node)):
        a = [p for p in adjacent(node[i]) if p[0] < size and p[1] < size and p[0] >= 0 and p[1] >= 0]
        #print(node[:i])
        #print(a)
        #print(node[i+1:])
        [output.append(node[:i] + tuple([p]) + node[i+1:]) for p in a]"""
    idk = []
    for i in range(len(node)):
        idk.append([p for p in adjacent(node[i]) if p[0] < size and p[1] < size and p[0] >= 0 and p[1] >= 0])
        idk[-1].append(node[i])
        idk[-1] = tuple(idk[-1])
    #Take all possible combinations
    #print(idk)
    output = all_possible_combinations(idk)
    return output

        

def main():
    agents = []
    goals = []
    colors = []
    g = nx.Graph()
    screen = pygame.display.set_mode((size*tileSize, size*tileSize))
    clock = pygame.time.Clock()

    for i in range(0, numAgents*floor(size/numAgents), floor(size/numAgents)):
        agents.append((0, random.choice([j for j in range(size) if j not in [aa[1] for aa in agents]])))
        goals.append((size-1, random.choice([j for j in range(size) if j not in [g[1] for g in goals]])))
        #colors.append(random.choices(list(pygame.color.THECOLORS.keys())))
        colors.append((random.randrange(256), random.randrange(256), random.randrange(256)))

    nodes_for_adding = []
    edges_for_adding = []
    #Generate a string containing code for an arbitrary number of nested for loops
    string = ""
    inner_string = "("
    p = inflect.engine()
    for i in range(len(agents)):
        inner_string += f"({p.number_to_words(i).strip().replace(" ", "_")}_i, {p.number_to_words(i).strip().replace(" ", "_")}_j), "
    inner_string += ")"

#    for i in range(len(agents)):
#        string = f"""{string}
#{"    "*i*2}for {p.number_to_words(i).strip().replace(" ", "_")}_i in range(size):
#{"    "*i*2}    for {p.number_to_words(i).strip().replace(" ", "_")}_j in range(size):"""
#    string = f"""{string}
#{"    "*len(agents)*2}if not contains_duplicates({inner_string}):
#{"    "*len(agents)*2}    nodes_for_adding.append({inner_string})"""

    for i in range(len(agents)):
        string = f"""{string}
{"    "*i*2}for {p.number_to_words(i).strip().replace(" ", "_")}_i in range(size):
{"    "*i*2}    for {p.number_to_words(i).strip().replace(" ", "_")}_j in range(size):"""
    string = f"""{string}
{"    "*len(agents)*2}if not contains_duplicates({inner_string}):
{"    "*len(agents)*2}    nodes_for_adding.append({inner_string})"""


    print(string)
    #Locals and globals stuff for exec()
    l = locals()
    print("Generating nodes...")
    exec(string, globals(), l)
    print(f"Nodes successfully generated! ({len(nodes_for_adding)} nodes total)")
    nodes_for_adding = l["nodes_for_adding"]
    print("Generating edges (will take even longer...)")
    try:
        for node in nodes_for_adding:
            [edges_for_adding.append((node, node2)) for node2 in all_potential_neighbors(node)]
    except KeyboardInterrupt:
        print()
        print(len(edges_for_adding), "edges generated before interrupt")
        exit()
    print(f"Edges successfully generated! ({len(edges_for_adding)} edges total)")
    """
    print("Adding nodes...")
    g.add_nodes_from(nodes_for_adding)
    print("Nodes added!")
    """
    #Since networkx automatically adds missing nodes when adding edges, I can skip adding the nodes beforehand.
    print("Adding nodes (and thus edges)...")
    g.add_edges_from(edges_for_adding)
    print("Edges added!")
    print("Generating path (paths)...")
    path = nx.shortest_path(g, tuple(agents), tuple(goals))

    step = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill("white")
        try:
            agents = path[step]
        except IndexError:
            pass
        print(agents)
        for i in range(len(agents)):
            thing = pygame.surface.Surface((tileSize, tileSize))
            thing.fill(colors[i])
            scaleFactor = 0.5
            thing = pygame.transform.scale_by(thing, scaleFactor)
            screen.blit(thing, (tileSize*agents[i][0] + tileSize*(1-scaleFactor)/2, tileSize*agents[i][1] + tileSize*(1-scaleFactor)/2))
            thing = pygame.transform.scale_by(thing, 1/scaleFactor)
            scaleFactor = 0.2
            thing = pygame.transform.scale_by(thing, scaleFactor)
            screen.blit(thing, (tileSize*goals[i][0] + tileSize*(1-scaleFactor)/2, tileSize*goals[i][1] + tileSize*(1-scaleFactor)/2))
        pygame.display.update()
        clock.tick(1)
        step += 1

if __name__ == "__main__":
    print()
    print()
    main()