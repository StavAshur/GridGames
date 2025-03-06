import random
import math

import matplotlib.pyplot as plt
import networkx as nx

def dist(start, end):
    return math.sqrt((start[0]-end[0])*(start[0]-end[0])+(start[1]-end[1])*(start[1]-end[1]))

class Grid:
    def __init__(self, n, m=None):
        if m is None:
            m = n
        self.n = n
        self.m = m
        self.grid = [[False for _ in range(m)] for _ in range(n)]
        self.graph = nx.grid_2d_graph(n, m)
    
    def block_cells(self, p):
        for i in range(self.n):
            for j in range(self.m):
                if random.random() < p:
                    self.grid[i][j] = True
                    self.graph.remove_node((i, j))
    
    def visualize_grid(self, wait_time=None):
        plt.figure(figsize=(10, 10))
        for i in range(self.n):
            for j in range(self.m):
                color = 'black' if self.grid[i][j] else 'white'
                plt.gca().add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, edgecolor='black', facecolor=color))
        plt.xlim(0, self.m)
        plt.ylim(0, self.n)
        plt.gca().set_aspect('equal', adjustable='box')
        if wait_time is not None:
            plt.show(block=False)
            #time.sleep(wait_time)
            plt.close()
        else:
          plt.show()
    
    def visualize_grid_with_colors(self, colored_cells, wait_time=None):
        plt.figure(figsize=(10, 10))
        for i in range(self.n):
            for j in range(self.m):
                color = 'black' if self.grid[i][j] else 'white'
                plt.gca().add_patch(plt.Rectangle((j, self.n - i - 1), 1, 1, edgecolor='black', facecolor=color))
        
        for (x, y, color) in colored_cells:
            plt.gca().add_patch(plt.Rectangle((y, self.n - x - 1), 1, 1, edgecolor='black', facecolor=color))
        
        plt.xlim(0, self.m)
        plt.ylim(0, self.n)
        plt.gca().set_aspect('equal', adjustable='box')
        if wait_time is not None:
            plt.show(block=False)
            #plt.pause(wait_time)
            # time.sleep(wait_time)
            plt.close()
        else:
          plt.show()
    
    def shortest_path(self, start, end):
        try:
            path = nx.shortest_path(self.graph, source=start, target=end)
            length = len(path) - 1
            return path, length
        except nx.NetworkXNoPath:
            return None, float('inf')

class Agent:
    def __init__(self, x, y, color, strategy):
        self.x = x
        self.y = y
        self.color = color
        self.strategy = strategy
        self.target = (None,None)

def random_walk_strategy(grid, x, y):
    neighbors = list(grid.graph.neighbors((x, y)))
    if neighbors:
        return (random.choice(neighbors), (None,None))
    return ((x, y), (None,None))

def shortest_path_strategy(grid, start, goal):
    if start == goal:
        return (start, start)
    path, _ = grid.shortest_path(start, goal)
    if path and len(path) > 1:
        return (path[1], goal)
    return (start, start)

def avoid_other_agents(grid, start, agents_positions):
    #Strategy:
    #Iterate over all enemies
    #Calculate path length from enemy to each corner (can be changed form corner to something else in possibleTargets)
    #Multiply that path length by the square of the exact distance 
    #from the first step along the path to that corner to the enemy
    #Navigate towards corner with the best score by this method
    possibleTargets = [(0,0), (grid.n-1,0), (grid.n-1, grid.m-1), (0, grid.m-1), (round(grid.n/2), round(grid.m/2))]
    best = 0
    bestDistance = 0
    for agent in agents_positions:
        bestDistance += grid.shortest_path(agent, possibleTargets[best])[1]
        #bestDistance += dist(start, agent)
        try:
            nextStep = grid.shortest_path(start, possibleTargets[best])[0][1]
            bestDistance *= dist(nextStep, agent)**3
        except:
            pass
    for i in range(len(possibleTargets)):
        target = possibleTargets[i]
        distance = 0
        for agent in agents_positions:
            distance += grid.shortest_path(agent, target)[1]
            distance += dist(target, agent)
            try:
                nextStep = grid.shortest_path(start, target)[0][1]
                distance *= dist(nextStep, agent)**3
            except:
                pass
        if(distance > bestDistance):
            best = i
            bestDistance = distance
    path = grid.shortest_path(start, possibleTargets[best])[0]
    if path and len(path) > 1:
        return (path[1], possibleTargets[best])
    return (start, start)
    



# Example usage:
# grid = Grid(5)
# grid.block_cells(0.3)
# grid.visualize_grid()
# colored_cells = [(0, 0, 'red'), (4, 4, 'blue')]
# grid.visualize_grid_with_colors(colored_cells)

# agent_random_walk = Agent(0, 0, 'green', random_walk_strategy)
# agent_shortest_path = Agent(0, 0, 'blue', shortest_path_strategy)

# # Move the agent with random walk strategy
# new_position_random_walk = agent_random_walk.strategy(grid, agent_random_walk.x, agent_random_walk.y)
# print("New position with random walk strategy:", new_position_random_walk)

# # Move the agent with shortest path strategy
# new_position_shortest_path = agent_shortest_path.strategy(grid, (agent_shortest_path.x, agent_shortest_path.y), (4, 4))
# print("New position with shortest path strategy:", new_position_shortest_path)

# path, length = grid.shortest_path((0, 0), (4, 4))
# print("Shortest path:", path)
# print("Path length:", length)
