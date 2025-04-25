import random
import networkx as nx
from time import sleep
import sys
#Import later
pygame = None

random.seed(1)

if "--terminal" not in sys.argv and "-t" not in sys.argv:
    import pygame
    globals()["pygame"] = pygame
    pygame.init()

def connections(char, pos):
    match char:
        case "-":
            #return [2, 0]
            return [(pos[0]+1, pos[1]), (pos[0]-1, pos[1])]
        case "◫":
            #return [3, 1]
            return[(pos[0], pos[1]+1), (pos[0], pos[1]-1)]
        case "◰":
            #return [3, 2]
            return [(pos[0]-1, pos[1]), (pos[0], pos[1]-1)]
        case "◳":
            #return [3, 0]
            return [(pos[0]+1, pos[1]), (pos[0], pos[1]-1)]
        case "◲":
            #return [1, 0]
            return [(pos[0]+1, pos[1]), (pos[0], pos[1]+1)]
        case "◱":
            #return [1, 2]
            return [(pos[0], pos[1]+1), (pos[0]-1, pos[1])]
        case "▦":
            return [(pos[0]+1, pos[1]),(pos[0], pos[1]+1),(pos[0]-1, pos[1]),(pos[0], pos[1]-1)]
        case _:
            return []

def adjacent(pos, size):
    return [p for p in [(pos[0]+1, pos[1]),(pos[0], pos[1]+1),(pos[0]-1, pos[1]),(pos[0], pos[1]-1)] if -1<p[0]<size and -1<p[1]<size]

def find_all_cycles(g):
    output = set()
    for node in g:
        try:
            s = set()
            for edge in nx.find_cycle(g, node):
                s.add(edge[0])
            output.add(tuple(s))
        except nx.NetworkXNoCycle:
            pass
    return output

def main():
    size = 50
    tileSize = 10
    if "--terminal" not in sys.argv and "-t" not in sys.argv:
        import pygame
        globals()["pygame"] = pygame
        pygame.init()
        screen = pygame.display.set_mode((50*tileSize, 50*tileSize))
        clock = pygame.time.Clock()
    counts = []
    sizes  = []
    for _ in range(1000):
        g = nx.Graph()
        character_dict = {}
        display = ""
        avg = 0
        for i in range(size):
            for j in range(size):
                char = random.choice(list("◫◰◱◲◳-▦"))
                g.add_node((i, j))
                character_dict.update({(i, j): char})
                display += char + " "
            display += "\n"
        for node1 in g:
            """
            for i in connections(character_dict[node1]):
                try:
                    node2 = adjacent(node1, size)[i]
                except:
                    continue
                #if (i+2)%4 in connections(character_dict[node2]):
                    #g.add_edge(node1, node2)
                for j in connections(character_dict[node2]):
                    try:
                        if node1 == adjacent(node2, size)[j]:
                            g.add_edge(node1, node2)
                    except:
                        pass"""
            for node2 in connections(character_dict[node1], node1):
                try:
                    if node1 in connections(character_dict[node2], node2):
                        g.add_edge(node1, node2)
                except KeyError:
                    pass
            
        """character_dict.update({
            (0, 0): "◫",
            (0, 1): "◲",
            (0, 2): "◱",
            (1, 1): "◱",
            (1, 2): "◫",
            (1, 3): "◰",
            (0, 3): "-",
            (0, 4): "◲",
            (1, 4): "◱"
        })"""
        if "--terminal" in sys.argv or "-t" in sys.argv:
            cycles = find_all_cycles(g)
            counts.append(len(cycles))
            for cycle in cycles:
                sizes.append(len(cycle))
            avg = 0
            avg2 = 0
            for c in counts:
                avg += c
            for s in sizes:
                avg2 += s
            avg /= len(counts)
            avg2 /= len(sizes)
            print(f"{display}\nTotal loops: {counts[-1]} \nAverage: {avg}\nAverage loop length: {avg2}")
            sleep(0.001)
        else:
            cycles = find_all_cycles(g)
            counts.append(len(cycles))
            for cycle in cycles:
                sizes.append(len(cycle))
            avg = 0
            avg2 = 0
            for c in counts:
                avg += c
            for s in sizes:
                avg2 += s
            avg /= len(counts)
            avg2 /= len(sizes)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill("white")
            for node in g.nodes:
                match character_dict[node]:
                    case "-":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                    case "◫":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                    case "◰":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize, node[1]*tileSize + tileSize/2))
                    case "◳":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                    case "◲":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                    case "◱":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                    case "▦":
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        pygame.draw.line(screen, "black", 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        pygame.draw.line(screen, "black", 
                                         (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                         (node[0]*tileSize, node[1]*tileSize + tileSize/2))
            for cycle in cycles:
                for node in cycle:
                    match character_dict[node]:
                        case "-":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        case "◫":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                        case "◰":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2))
                        case "◳":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        case "◲":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                        case "◱":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                        case "▦":
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2), 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize + tileSize))
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize + tileSize, node[1]*tileSize + tileSize/2))
                            pygame.draw.line(screen, "red", 
                                            (node[0]*tileSize + tileSize/2, node[1]*tileSize), 
                                            (node[0]*tileSize, node[1]*tileSize + tileSize/2))
                    #print(node, character_dict[node], g.adj[node])
            pygame.display.set_caption(f"Total loops: {counts[-1]} Average: {round(avg*10000)/10000}{" "*(4-len(str(round(avg*10000)/10000)))} Average loop length: {round(avg2*10000)/10000}{" "*(4-len(str(round(avg2*10000)/10000)))}") 
            pygame.display.update()
            clock.tick(60)
            


if __name__ == "__main__":
    main()