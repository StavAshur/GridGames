"‾‾";"| ";" |";"__";"  ";""
import networkx as nx
from random import randint, choice
from graph_utilities import convert_grid, adjacent
import pygame
from sys import exit


def print_grid(g, width=None, height=None):
    if not width:
        width = sorted(g.nodes, key=lambda x: x[0])[-1][0]
    if not height:
        height = sorted(g.nodes, key=lambda x: x[1])[-1][1]
    output = ""
    for row in convert_grid(g):
        for node in row:
            d = False
            u = False
            l = False
            r = False
            if (node[0]-1, node[1]) in g.adj[node]:
                l = True
            if (node[0]+1, node[1]) in g.adj[node]:
                r = True
            if (node[0], node[1]-1) in g.adj[node]:
                u = True
            if (node[0], node[1]+1) in g.adj[node]:
                d = True
            match (u, r, d, l):
                case (False, False, False, False):
                    output += "⃞ "
                case (True, True, True, True):
                    output += "  "
                case (False, True, True, True):
                    output += "‾‾"
                case (True, True, False, True):
                    output += "__"
                case (True, False, True, True):
                    output += " │"
                case (True, True, True, False):
                    output += "│ "
                case (True, False, True, False):
                    output += "││"
                case (False, True, False, True) | (False, False, False, True) | (False, True, False, False):
                    if node[1] == 0:
                        output += "‾‾"
                    elif node[1] == height:
                        output += "__"
                    elif output.splitlines()[node[1]-1][node[0]*2:node[0]*2+2] == "‾‾":
                        output += "‾‾"
                    else:
                        output += "__"
                case (False, False, True, True):
                    output += "‾│"
                case (False, True, True, False):
                    output += "│‾"
                case (True, True, False, False):
                    output += "│_"
                case (True, False, False, True):
                    output += "_│"
                case (False, False, True, False):
                    output += "┌┐"
                case (True, False, False, False):
                    output += "└┘"
                #case (False, False, False, True):
                #    output += " ב"
                case _:
                    output += "  "
            if node[0] == width:
                output += "\n"
    
    print(output)

def draw_cell_borders(grid, surface, cellSize, color="black"):
    s = cellSize
    for row in convert_grid(g):
        for node in row:
            #d = False
            #u = False
            #l = False
            #r = False
            if node not in g:
                continue
            if (node[0]-1, node[1]) not in g.adj[node]:
                #l = True
                pygame.draw.line(surface, color, (node[0]*s, node[1]*s), (node[0]*s, node[1]*s+s))
            if (node[0]+1, node[1]) not in g.adj[node]:
                #r = True
                pygame.draw.line(surface, color, (node[0]*s+s, node[1]*s), (node[0]*s+s, node[1]*s+s))
            if (node[0], node[1]-1) not in g.adj[node]:
                #u = True
                pygame.draw.line(surface, color, (node[0]*s, node[1]*s), (node[0]*s+s, node[1]*s))
            if (node[0], node[1]+1) not in g.adj[node]:
                #d = True
                pygame.draw.line(surface, color, (node[0]*s, node[1]*s+s), (node[0]*s+s, node[1]*s+s))
            """
            match (u, r, d, l):
                case (False, False, False, False):
                    pygame.draw.line(surface, color, (node[0], node[1]), (node[0]+cellSize, node[1]))
                    pygame.draw.line(surface, color, (node[0], node[1]), (node[0], node[1]+cellSize))
                    pygame.draw.line(surface, color, (node[0]+cellSize, node[1]), (node[0]+cellSize, node[1]+cellSize))
                    pygame.draw.line(surface, color, (node[0], node[1]+cellSize), (node[0]+cellSize, node[1]+cellSize))
                case (True, True, True, False):
                    pygame.draw.line(surface, color, (node[0], node[1]), (node[0], node[1]+cellSize))
                case (True, True, True, False):
                    pygame.draw.line(surface, color, (node[0], node[1]+cellSize), (node[0]+cellSize, node[1]+cellSize))
                case ()"""

def origin_shift(g, origin):
    g2 = nx.dfs_tree(g, origin).reverse()
    new_origin = choice([n for n in adjacent(origin) if n in list(g.nodes)])
    [g2.remove_edge(new_origin, node) for node in list(g2.adj[new_origin])]
    g2.add_edge(origin, new_origin)
    return (nx.Graph(g2), new_origin)

size = 50
cellSize = 20

pygame.init()
screen = pygame.display.set_mode((size*cellSize+10, size*cellSize+10))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()
g = nx.grid_2d_graph(size, size)
g = nx.Graph(nx.dfs_tree(g, (0, 0)))
origin = (0, 0)
go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = False
    key = pygame.key.get_pressed()
    screen.fill("white")
    temp = pygame.surface.Surface(screen.get_size())
    temp.fill("white")
    draw_cell_borders(g, temp, cellSize)
    screen.blit(temp, (0, 1))
    #pygame.draw.circle(screen, "red", (origin[0]*10+5, origin[1]*10+5), 5)
    pygame.display.update()
    g, origin = origin_shift(g, origin)
temp = pygame.image.tobytes(screen, "RGBA")
pygame.display.set_mode((1, 1))
if input("Save maze? (type 'y' or 'yes' and press enter to save) ").lower().strip() in ["y", "yes"]:
    pygame.image.save(pygame.image.frombytes(temp, (size*cellSize+10, size*cellSize+10), "RGBA"), "maze.png")
pygame.quit()
