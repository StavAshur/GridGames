import random
import matplotlib.pyplot as plt
import networkx as nx

# Step 1: Generate a 100x100 grid
grid_size = 20
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

# Step 2: Turn cells into obstacles with probability 1/100
for i in range(grid_size):
    for j in range(grid_size):
        if random.random() < 0.01:
            grid[i][j] = 1  # 1 represents an obstacle

# Step 3: Prompt the user for a mine probability
p = float(input("Enter the probability of a mine (0 to 1): "))

# Step 4: Turn remaining cells into mines with probability p, ensuring no adjacent mines
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == 0:  # Only consider free cells
            if random.random() < p:
                # Check adjacent cells
                adjacent_mines = False
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < grid_size and 0 <= nj < grid_size and grid[ni][nj] == 2:
                            adjacent_mines = True
                            break
                    if adjacent_mines:
                        grid[i][j] = 2
                if not adjacent_mines:
                    grid[i][j] = 2  # 2 represents a mine

# Display the grid with obstacles and mines
plt.figure(figsize=(10, 10))
for i in range(grid_size):
    for j in range(grid_size):
        if grid[i][j] == 1:
            color = 'black'  # Obstacle
        elif grid[i][j] == 2:
            color = 'red'  # Mine
        else:
            color = 'white'  # Free cell
        plt.gca().add_patch(plt.Rectangle((j, grid_size - i - 1), 1, 1, edgecolor='black', facecolor=color))
plt.xlim(0, grid_size)
plt.ylim(0, grid_size)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
