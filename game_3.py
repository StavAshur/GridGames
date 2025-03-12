import random
import matplotlib.pyplot as plt
from grid import Grid, Agent, random_walk_strategy, shortest_path_strategy, avoid_other_agents, dist
import networkx
from sys import exit
import time

def random_walk_new(grid, selfPos, chasers, runners): return random_walk_strategy(grid, selfPos[0], selfPos[1])[0]
def shortest_path_new(grid, selfPos, chasers, runners): return shortest_path_strategy(grid, selfPos, (runners[0].x, runners[0].y))[0]
def avoid_other_agents_new(grid, selfPos, chasers, runners): return avoid_other_agents(grid, selfPos, [(a.x, a.y) for a in chasers])[0]
class InitializationError(Exception):
    def __init__(self, parameter, value, message):
        self.message = message
        super().__init__(self.message)
        self.parameter = parameter
        self.value = value
    
    def __str__(self):
        return f"InitializationError: Parameter \"{self.parameter}\" at value {self.value} invalid: {self.message}"

class Simulation:
    def __init__(self, size, chaserStrategies, runnerStrategies):
        if(size < 5 or type(size) != int):
            raise InitializationError("size", size, "Should be an int greater than 4")
        self.size = size
        self.grid = Grid(size)
        self.grid.block_cells(0.1)
        self.grid.grid[0][0] = False
        self.grid.grid[size-1][0] = False
        self.grid.grid[0][size-1] = False
        self.grid.grid[size-1][size-1] = False
        free_cells = [(i, j) for i in range(self.size) for j in range(self.size) if not self.grid.grid[i][j]]
        self.chasers = []
        for strategy in chaserStrategies:
            pos = random.choice(free_cells)
            #lambda strategy
            #grid, (selfPos), [chasers], [runners] -> (nextPos)
            self.chasers.append(Agent(pos[0], pos[1], "blue", strategy))
        for strategy in runnerStrategies:
            pos = random.choice(free_cells)
            self.runners.append(Agent(pos[0], pos[1], "red", strategy))
        self.doneStates.append((self.runners, self.chasers))
    def update(self):
        new_runner_positions = [runner.strategy(self.grid, (runner.x, runner.y), self.chasers, self.runners) for runner in self.runners]
        new_chaser_positions = [chaser.strategy(self.grid, (chaser.x, chaser.y), self.chasers, self.runners) for chaser in self.chasers]
        for runner in self.runners: runner

        


def main():
    try:
        s = Simulation(int(input("Size: ")), [shortest_path_new], [avoid_other_agents_new])
        while True: s.update()
    except networkx.nodeNotFound:
        main()
    except KeyboardInterrupt:
        exit(": Manually terminated")
