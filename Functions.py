import random
import textwrap

def create_random_obstacles(grid_world, density):
    total_blocks = grid_world.m * grid_world.n
    number_of_walls = int(density * total_blocks)
    for i in range(number_of_walls):
        x = random.randint(0, grid_world.m - 1)
        y = random.randint(0, grid_world.n - 1)
        if not ((x == grid_world.start_x and y == grid_world.start_y) or (
                x == grid_world.end_x and y == grid_world.end_y)):
            grid_world.obstacles.add((x, y))