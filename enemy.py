import random
from queue import PriorityQueue

import pygame

from utils import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, app, pos, type):
        self.app = app
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/blinky.png').convert()
        self.image = pygame.transform.scale(self.image, (self.app.cell_width, self.app.cell_height))
        self.grid_pos = pos
        self.type = type
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width // 2.3)
        self.direction = vec(0, 0)
        self.target = None
        self.speed = 1

    def update(self):
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

    def time_to_move(self):
        if int(self.pix_pos.x + 25) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + 25) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.type == 'random':
            self.direction = self.get_random_direction()
        else:
            self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        global path
        if self.app.player.current_alg == 'DFS':
            path = self.app.graph_alg.DFS([int(self.grid_pos[0]), int(self.grid_pos[1])], [
                int(target[0]), int(target[1])])
        elif self.app.player.current_alg == 'BFS':
            path = self.app.graph_alg.BFS([int(self.grid_pos[0]), int(self.grid_pos[1])], [
                int(target[0]), int(target[1])])
        elif self.app.player.current_alg == 'UCS':
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
