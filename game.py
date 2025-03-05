import time
import random
import matplotlib.pyplot as plt
from grid import Grid, Agent, random_walk_strategy

def run_simulation():
    # Create a 50x50 grid with blocked cell probability of 0.1
    grid = Grid(50)
    grid.block_cells(0.1)

    # Initialize two agents with random free starting positions
    free_cells = [(i, j) for i in range(50) for j in range(50) if not grid.grid[i][j]]
    start_pos1 = random.choice(free_cells)
    free_cells.remove(start_pos1)
    start_pos2 = random.choice(free_cells)

    agent1 = Agent(start_pos1[0], start_pos1[1], 'blue', random_walk_strategy)
    agent2 = Agent(start_pos2[0], start_pos2[1], 'red', random_walk_strategy)

    while True:
        # Visualize the current state of the grid with agents
        colored_cells = [(agent1.x, agent1.y, agent1.color), (agent2.x, agent2.y, agent2.color)]
        grid.visualize_grid_with_colors(colored_cells)

        # Move agents according to their strategy
        new_pos1 = agent1.strategy(grid, agent1.x, agent1.y)
        new_pos2 = agent2.strategy(grid, agent2.x, agent2.y)

        agent1.x, agent1.y = new_pos1
        agent2.x, agent2.y = new_pos2

        # Wait for 0.3 seconds before the next turn
        plt.pause(0.3)
        plt.clf()

if __name__ == "__main__":
    run_simulation()