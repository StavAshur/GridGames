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

# Step 5: Prompt the user for a threshold k
k = int(input("Enter the threshold k (number of mines allowed): "))

# Step 6: Create a directed graph with k layers using networkx
G = nx.DiGraph()

# Add nodes and edges for each layer
for layer in range(k + 1):
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] != 1:  # Skip obstacles
                G.add_node((i, j, layer))
                # Add edges for possible motions
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < grid_size and 0 <= nj < grid_size and grid[ni][nj] != 1:
                        if grid[ni][nj] == 2 and layer < k:  # Mine encountered
                            G.add_edge((i, j, layer), (ni, nj, layer + 1))
                        elif grid[ni][nj] != 2:  # Free cell
                            G.add_edge((i, j, layer), (ni, nj, layer))
                            G.add_edge((i, j, layer), (ni, nj, layer + 1))

# Display the number of nodes and edges in the graph
print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")


# Step 7: Prompt the user for start and target positions
s_x = int(input("Enter the start x-coordinate (0 to n-1): ")) 
s_y = int(input("Enter the start y-coordinate (0 to n-1): "))
t_x = int(input("Enter the target x-coordinate (0 to n-1): "))
t_y = int(input("Enter the target y-coordinate (0 to n-1): "))
# For demonstration, let's use fixed start and target positions
# s_x, s_y = 0, 0  # Example start position
# t_x, t_y = 99, 99  # Example target position

# Step 8: Find a path from (s_x, s_y, 0) to (t_x, t_y, k)
try:
    path = nx.shortest_path(G, source=(s_x, s_y, 0), target=(t_x, t_y, k))
    print("Path found:", path)
except nx.NetworkXNoPath:
    print("No path found.")


# Step 9: Animate the path
plt.figure(figsize=(10, 10))
for step, (x, y, layer) in enumerate(path):
    plt.clf()
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == 1:
                color = 'black'  # Obstacle
            elif grid[i][j] == 2:
                color = 'red'  # Mine
            else:
                color = 'white'  # Free cell
            plt.gca().add_patch(plt.Rectangle((j, grid_size - i - 1), 1, 1, edgecolor='black', facecolor=color))
    plt.gca().add_patch(plt.Rectangle((y, grid_size - x - 1), 1, 1, edgecolor='blue', facecolor='blue'))
    plt.xlim(0, grid_size)
    plt.ylim(0, grid_size)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(f"Step {step + 1}/{len(path)}")
    plt.pause(0.1)
plt.show()