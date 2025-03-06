import random
import matplotlib.pyplot as plt
from grid import Grid, Agent, random_walk_strategy, shortest_path_strategy, avoid_other_agents, dist
import networkx
from sys import exit
import time

def run_simulation(gridSize):
    try:
        # Create a 50x50 grid with blocked cell probability of 0.1
        grid = Grid(gridSize)
        grid.block_cells(0.1)
        grid.grid[0][0] = False
        grid.grid[gridSize-1][0] = False
        grid.grid[0][gridSize-1] = False
        grid.grid[gridSize-1][gridSize-1] = False
        
        # Initialize two agents with random free starting positions
        free_cells = [(i, j) for i in range(gridSize) for j in range(gridSize) if not grid.grid[i][j]]
        start_pos1 = random.choice(free_cells)
        free_cells.remove(start_pos1)
        start_pos2 = random.choice(free_cells)
        
        agent1 = Agent(start_pos1[0], start_pos1[1], 'blue', shortest_path_strategy)
        agent2 = Agent(start_pos2[0], start_pos2[1], 'red', avoid_other_agents)

        doneStates = [((agent1.x, agent1.y), (agent2.x, agent2.y))]

        # Create the figure and axis objects
        fig, ax = plt.subplots(figsize=(10, 10))
        while True:
            # Clear the previous plot
            ax.clear()

            # Visualize the current state of the grid with agents
            for i in range(grid.n):
                for j in range(grid.m):
                    color = 'black' if grid.grid[i][j] else 'white'
                    ax.add_patch(plt.Rectangle((j, grid.n - i - 1), 1, 1, edgecolor='black', facecolor=color))
            
            for (x, y, color) in [(agent1.x, agent1.y, agent1.color), (agent2.x, agent2.y, agent2.color)]:
                ax.add_patch(plt.Rectangle((y, grid.n - x - 1), 1, 1, edgecolor='black', facecolor=color))
            
            #Add special graphics
            path, _ = grid.shortest_path((agent1.x, agent1.y), (agent2.x, agent2.y))
            target_2 = agent2.strategy(grid, (agent2.x, agent2.y), [(agent1.x, agent1.y)])[1]
            #Visualize chaser path in yellow
            if path:
                for (x, y) in path[1:-1]:
                    ax.add_patch(plt.Rectangle((y, grid.n - x - 1), 1, 1, edgecolor='black', facecolor='yellow'))
            #Show runner target corner
            ax.add_patch(plt.Rectangle((target_2[1], grid.n - target_2[0] - 1), 1, 1, edgecolor='black', facecolor='red'))
            #Show shortest path from chaser to that corner (used to calculate runner decisions) (commented out by default)
            #path, _ = grid.shortest_path((agent1.x, agent1.y), (target_2[0], target_2[1]))
            #if path:
                #for (x, y) in path[1:-1]:
                    #ax.add_patch(plt.Rectangle((y+0.40, grid.n - x - 0.60), 0.2, 0.2, edgecolor='black', facecolor='blue'))
            #Show runner path
            path, _ = grid.shortest_path((agent2.x, agent2.y), (target_2[0], target_2[1]))
            if path:
                for (x, y) in path[1:-1]:
                    ax.add_patch(plt.Rectangle((y+0.40, grid.n - x - 0.60), 0.2, 0.2, edgecolor='black', facecolor='red'))
            
            ax.set_xlim(0, grid.m)
            ax.set_ylim(0, grid.n)
            ax.set_aspect('equal', adjustable='box')

            # Display the plot
            plt.show(block=False)
            #Add small delay to simulation to prevent odd bugs
            plt.pause(0.1)

            # Move agents according to their strategy
            new_pos1 = agent1.strategy(grid, (agent1.x, agent1.y), (agent2.x, agent2.y))[0]
            new_pos2 = agent2.strategy(grid, (agent2.x, agent2.y), [(agent1.x, agent1.y)])[0]

            #Check if chaser wins
            if(dist((agent1.x, agent1.y), (agent2.x, agent2.y)) <= 1):
                print("Chaser wins in", len(doneStates), "steps")
                time.sleep(1)
                exit()
            if((new_pos1, new_pos2) in doneStates):
                print("Runner wins in", len(doneStates), "steps")
                exit()
            else:
                doneStates.append((new_pos1, new_pos2))
            

            try:
                agent1.x, agent1.y = new_pos1
                agent2.x, agent2.y = new_pos2
            except TypeError:
                print(new_pos1, new_pos2)
    except networkx.NodeNotFound:
        print("networkx.NodeNotFound error! Resetting")
        run_simulation(gridSize)
    except KeyboardInterrupt:
        exit(": Manually terminated")


if __name__ == "__main__":
    run_simulation(20)