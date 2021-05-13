import time
import tkinter as tk
import random
import numpy as np

from Graph import Graph


class GridWorld:
    
    def __init__(self, m=20, n=20, start_x = 0, start_y = 0, end_x = 0, end_y=0):
        self.height = 700
        self.width = 700
        self.agent = ()
        self.agent_ui = ()
        self.length = 0
        self.possible_moves = ()
        self.agent_padding = 0
        self.dfs_route = []
        self.dfs_best_route = []
        self.route = []
        self.final_route_genetic = []
        self.a_star_route = []
        self.a_star_final_route = []
        self.aco_current_route = []
        self.aco_best_route = []
        self.padding = 30
        self.current_estimates = []
        self.a_star_visited_count = 0
        self.a_star_opened_count = 0

        self.m = m
        self.n = n
        self.is_visited = [[0] * self.m for temp in range(self.n)]

        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.start_key = str(self.start_x) + "," + str(self.start_y)
        self.graph = Graph(self.start_key)

        self.obstacles = set()

        self.color_background = 'white'
        self.color_walls = '#d50000'
        self.color_normal = 'white'
        window = tk.Tk()
        window.title("Q-Learning ile Yol Planlaması")
        self.frame = tk.Canvas(bg=self.color_background, height=self.height, width=self.height)
        self.frame.pack()

    def create_grid_ui(self, m, n, start, end, obstacles):
        l1 = (self.width - (2 * self.padding)) / m
        l2 = (self.height - (2 * self.padding)) / n
        length = min(l1, l2)
        self.length = length
        self.agent_padding = 0.1 * length
        for i in range(m):
            for j in range(n):
                color = self.color_normal
                if (i, j) in self.obstacles:
                    color = self.color_walls
                if start == (i, j):
                    color = '#1E88E5'
                if end == (i, j):
                    color = '#388E3C'
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill=color)
        self.update_agent_ui((self.start_x, self.start_y))
        self.frame.update()

    def update_agent_ui(self, agent):
        length = self.length
        self.frame.delete(self.agent_ui)
        self.agent = agent
        self.agent_ui = self.frame.create_oval(
            ((length * agent[0]) + self.padding + self.agent_padding,
             (length * agent[1]) + self.padding + self.agent_padding),
            ((length * agent[0]) + length + self.padding - self.agent_padding,
             (length * agent[1]) + length + self.padding - self.agent_padding),
            fill='#FFD600')
        self.frame.update()

    def scan_grid_and_generate_graph(self):
        self.possible_moves = [[tuple()] * self.m for temp in range(self.n)]
        for i in range(self.m):
            for j in range(self.n):
                if (i, j) not in self.obstacles:
                    east = True
                    west = True
                    north = True
                    south = True
                    if i == 0:
                        west = False
                    if i == self.m - 1:
                        east = False
                    if j == 0:
                        north = False
                    if j == self.n - 1:
                        south = False
                    if (i + 1, j) in self.obstacles:
                        east = False
                    if (i - 1, j) in self.obstacles:
                        west = False
                    if (i, j + 1) in self.obstacles:
                        south = False
                    if (i, j - 1) in self.obstacles:
                        north = False
                    self.possible_moves[i][j] = (east, west, north, south)
                    self.graph.adjacency_map[str(i) + ',' + str(j)] = []
                    if east:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i + 1, j))
                    if west:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i - 1, j))
                    if north:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j - 1))
                    if south:
                        self.graph.adjacency_map[str(i) + ',' + str(j)].append((i, j + 1))

    def print_graph(self):
        graph = self.graph
        for k in graph.adjacency_map:
            print(k + " -> ", end='')
            for l in graph.adjacency_map[k]:
                print(str(l[0]) + "," + str(l[1]) + " : ", end='')
            print()

    def get_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - self.end_x)
        y1 = abs(y - self.end_y)
        return x1 + y1

    def get_reverse_heuristics(self, x, y):
        # manhattan distance
        x1 = abs(x - self.start_x)
        y1 = abs(y - self.start_y)
        return x1 + y1

    def save_graph(self):
        graph_code = ""
        for i in range(self.m):
            for j in range(self.n):
                if (i, j) in self.obstacles:
                    graph_code += '1'
                else:
                    graph_code += '0'
        print(hex(int(graph_code, 2)))
        return hex(int(graph_code, 2))

    def step(self, action):
        self.render()
        previous_state = (self.agent[0], self.agent[1])
        directions = ['east', 'west', 'north', 'south']
        move = directions[action]
        is_move_possible = False
        if move == 'east':
            if self.possible_moves[self.agent[0]][self.agent[1]][0]:
                self.agent = (self.agent[0] + 1, self.agent[1])
                self.update_agent_ui(self.agent)
                is_move_possible = True
        if move == 'west':
            if self.possible_moves[self.agent[0]][self.agent[1]][1]:
                self.agent = (self.agent[0] - 1, self.agent[1])
                self.update_agent_ui(self.agent)
                is_move_possible = True
        if move == 'north':
            if self.possible_moves[self.agent[0]][self.agent[1]][2]:
                self.agent = (self.agent[0], self.agent[1] - 1)
                self.update_agent_ui(self.agent)
                is_move_possible = True
        if move == 'south':
            if self.possible_moves[self.agent[0]][self.agent[1]][3]:
                self.agent = (self.agent[0], self.agent[1] + 1)
                self.update_agent_ui(self.agent)
                is_move_possible = True

        self.frame.tag_raise(self.agent)
        current_state = (self.agent[0], self.agent[1])

        # reward function
        if current_state == (self.end_x, self.end_y):
            reward = 5
            done = True
        elif current_state in self.obstacles:
            reward = -5
            done = True
        elif not is_move_possible:
            reward = -5
            done = False
        else:
            old_distance = self.get_reverse_heuristics(previous_state[0], previous_state[1])
            new_distance = self.get_reverse_heuristics(current_state[0], current_state[1])
            reward = 3  # new_distance - old_distance
            done = False
            if self.is_visited[current_state[0]][current_state[1]] > 0:
                reward = -self.is_visited[current_state[0]][current_state[1]]

        return current_state, reward, done

    def reset(self):
        self.frame.update()
        time.sleep(0.5)

        self.update_agent_ui((self.start_x, self.start_y))

        self.render()

        state = (self.agent[0], self.agent[1])
        return state

    def render(self):
        time.sleep(0.05)
        self.frame.update()

    def print_grid(self):
        file = open("matris.txt", "w")
        for i in range(self.m):
            for j in range(self.n):
                if(i, j) in self.obstacles:
                    file.write(str(j) + ',' + str(i) + ',K' + '\n')
                else:
                    file.write(str(j) + ',' + str(i) + ',B' + '\n')
        file.close()

    def print_final_route(self, final_route_x = [], final_route_y = []):
        final_route_x = final_route_x
        final_route_y = final_route_y
        len_array = len(final_route_x)
        length = self.length

        for x in range(len_array):
            time.sleep(0.01)
            i = final_route_x[x]
            j = final_route_y[x]
            if not (i == self.start_x and j == self.start_y) and not (i == self.end_x and j == self.end_y):
                self.frame.create_rectangle(i * length + self.padding, j * length + self.padding,
                                            i * length + self.padding + length,
                                            j * length + self.padding + length, fill='#7C4DFF')
            self.frame.update()