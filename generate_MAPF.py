import numpy as np
import matplotlib.pyplot as plt
import random

# Modified function to generate the grid
# (same as before, no change needed here)
def generate_mapf_grid(n, m, k):
    grid = -1 * np.ones((n, n), dtype=int)
    
    # Create horizontal corridors
    horizontal_rows = np.linspace(0, n-1, m, dtype=int)
    for row in horizontal_rows:
        grid[row, :] = 0
    
    # Create vertical corridors
    vertical_cols = np.linspace(0, n-1, k, dtype=int)
    for col in vertical_cols:
        grid[:, col] = 0
    
    # Assign start and goal positions
    starts = [(row, 0) for row in horizontal_rows]
    goals = [(row, n-1) for row in horizontal_rows]
    random.shuffle(goals)
    
    for i in range(m):
        grid[starts[i][0], starts[i][1]] = i + 1
        grid[goals[i][0], goals[i][1]] = m + i + 1
    
    return grid

# Modified plotting function to add outlines and ensure colors of i and m+i are the same
def save_and_plot_grid(grid, m):
    np.savetxt('MAPF.txt', grid, fmt='%d')
    
    cmap = plt.cm.get_cmap('tab20', m)  # Only m colors needed, since i and m+i share color
    color_grid = np.zeros((*grid.shape, 3))
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            val = grid[i,j]
            if val == -1:
                color_grid[i,j] = [0,0,0]  # Black obstacles
            elif val == 0:
                color_grid[i,j] = [1,1,1]  # White traversable
            elif 1 <= val <= m:
                color_grid[i,j] = cmap(val-1)[:3]
            elif m < val <= 2*m:
                color_grid[i,j] = cmap(val - m - 1)[:3]
    
    fig, ax = plt.subplots()
    ax.imshow(color_grid, interpolation='none')
    
    # Add grid lines for outlines
    ax.set_xticks(np.arange(-0.5, grid.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, grid.shape[0], 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
    
    ax.axis('off')
    plt.show()

# Example usage
n, m, k = 20, 6, 4
grid = generate_mapf_grid(n, m, k)
save_and_plot_grid(grid, m)