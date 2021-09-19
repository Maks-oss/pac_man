import random
from queue import PriorityQueue

import pygame

from utils import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, app, pos, color):
        self.app = app
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/blinky.png').convert()
        self.image = pygame.transform.scale(self.image, (self.app.cell_width, self.app.cell_height))
        self.grid_pos = pos
        self.color = color
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width // 2.3)
        self.direction = vec(0, 0)
        self.target = None
        self.speed = 1

    def update(self):
        # self.target = self.set_target()
        self.target = self.app.player.grid_pos
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - 50 +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - 50 +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self, screen):
        screen.blit(self.image, (self.pix_pos.x - 10,
                                 self.pix_pos.y - 10))

    def set_target(self):

        if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
            return vec(1, 1)
        if self.app.player.grid_pos[0] > COLS // 2 and self.app.player.grid_pos[1] < ROWS // 2:
            return vec(1, ROWS - 2)
        if self.app.player.grid_pos[0] < COLS // 2 and self.app.player.grid_pos[1] > ROWS // 2:
            return vec(COLS - 2, 1)
        else:
            return vec(COLS - 2, ROWS - 2)

    def time_to_move(self):

        if int(self.pix_pos.x + 25) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + 25) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        path = self.app.graph_alg.UCS([int(self.grid_pos[0]), int(self.grid_pos[1])], [
            int(target[0]), int(target[1])])
        return path[1]
    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos[0] + x_dir, self.grid_pos[1] + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + 25 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) + 25 +
                   self.app.cell_height // 2)

    # def UCS(self,start,target):
    #     grid = [[0 for x in range(28)] for x in range(30)]
    #     for cell in self.app.walls:
    #         if cell.x < 28 and cell.y < 30:
    #             grid[int(cell.y)][int(cell.x)] = 1
    #     queue = PriorityQueue()
    #     queue.put((0, [start]))
    #     visited=[]
    #     while not queue.empty():
    #         pair = queue.get()
    #         current = pair[1][-1]
    #         cost=pair[0]
    #         if current == target:
    #             return pair[1]
    #         neighbours = [[int(current[0] + 1), int(current[1])],
    #                       [int(current[0] - 1), int(current[1])],
    #                       [int(current[0]), int(current[1] + 1)],
    #                       [int(current[0]), int(current[1] - 1)]]
    #         for neighbour in neighbours:
    #             if 0 <= neighbour[0] < len(grid[0]):
    #                 if 0 <= neighbour[1] < len(grid):
    #                     next_cell = [int(neighbour[0]), int(neighbour[1])]
    #                     if grid[int(next_cell[1])][next_cell[0]] != 1 and next_cell not in visited:
    #                         visited.append(next_cell)
    #                         temp = pair[1][:]
    #                         temp.append(next_cell)
    #                         queue.put((cost+self.cost_function(next_cell,target), temp))
    #
    # def cost_function(self,point, end):
    #     return pow(point[0] - end[0], 2) + pow(point[1] - end[1], 2)
    #
    # def BFS(self, start, target):
    #     grid = [[0 for x in range(28)] for x in range(30)]
    #     for cell in self.app.walls:
    #         if cell.x < 28 and cell.y < 30:
    #             grid[int(cell.y)][int(cell.x)] = 1
    #     queue = [(start, [start])]
    #     visited = []
    #     while queue:
    #         (current, path) = queue.pop(0)
    #         visited.append(current)
    #         neighbours = [[int(current[0] + 1), int(current[1])],
    #                       [int(current[0] - 1), int(current[1])],
    #                       [int(current[0]), int(current[1] + 1)],
    #                       [int(current[0]), int(current[1] - 1)]]
    #         for neighbour in neighbours:
    #             if 0 <= neighbour[0] < len(grid[0]):
    #                 if 0 <= neighbour[1] < len(grid):
    #                     next_cell = [int(neighbour[0]), int(neighbour[1])]
    #                     if grid[int(next_cell[1])][next_cell[0]] != 1:
    #                         if next_cell == target:
    #                             return path + [target]
    #                         else:
    #                             if next_cell not in visited:
    #                                 visited.append(next_cell)
    #                                 queue.append((next_cell, path + [next_cell]))
    #
    #
    # def DFS(self, start, target):
    #     grid = [[0 for x in range(28)] for x in range(30)]
    #     for cell in self.app.walls:
    #         if cell.x < 28 and cell.y < 30:
    #             grid[int(cell.y)][int(cell.x)] = 1
    #     stack = [(start, [start])]
    #     visited = []
    #     while stack:
    #         (current, path) = stack.pop()
    #         if current not in visited:
    #             if current == target:
    #                 return path
    #             visited.append(current)
    #             neighbours = [[int(current[0] + 1), int(current[1])],
    #                           [int(current[0] - 1), int(current[1])],
    #                           [int(current[0]), int(current[1] + 1)],
    #                           [int(current[0]), int(current[1] - 1)]]
    #             for neighbour in neighbours:
    #                 if 0 <= neighbour[0] < len(grid[0]):
    #                     if 0 <= neighbour[1] < len(grid):
    #                         next_cell = [int(neighbour[0]), int(neighbour[1])]
    #                         if grid[int(next_cell[1])][next_cell[0]] != 1:
    #                             stack.append((next_cell, path + [next_cell]))
