import random

import pygame

from utils import *

vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        self.app = app
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pac.png').convert()
        self.image = pygame.transform.scale(self.image, (self.app.cell_width, self.app.cell_height))
        self.grid_pos = pos
        self.old_path = []
        self.previous_grid_pos = pos
        self.current_alg = 'UCS'
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        # self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 1

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.is_moving():
            # if self.stored_direction is not None:
            #     self.direction = self.stored_direction
            self.able_to_move = self.can_move()
            self.move()

        self.grid_pos[0] = (self.pix_pos[0] - 50 +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - 50 +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        if self.grid_pos == self.app.target_point:
            self.app.set_point()
            self.app.draw_point()
            pygame.display.update()
        if self.on_coin():
            self.eat_coin()

    def draw(self, screen):
        screen.blit(self.image, (self.pix_pos.x - 10,
                                 self.pix_pos.y - 10))
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20 * x, HEIGHT - 15), 7)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + 25) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + 25) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def change_algorithm(self):
        if self.current_alg == 'DFS':
            self.current_alg = 'BFS'
        elif self.current_alg == 'BFS':
            self.current_alg = 'UCS'
        elif self.current_alg == 'UCS':
            self.current_alg = 'DFS'

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        # print("direction:",vec(xdir,ydir))
        return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        if self.old_path:
            for p in self.old_path:
                pygame.draw.rect(self.app.maze, BLACK, p)
            self.old_path = []
        # print("Target ",self.app.target_point,"Player pos: ",self.grid_pos)
        path = self.app.graph_alg.a_star(self.grid_pos,target)
        # print(path)
        for p in path:
            self.old_path.append((p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                  self.app.cell_width // 2, self.app.cell_height // 2))
            pygame.draw.rect(self.app.maze, PLAYER_COLOUR, (p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                                            self.app.cell_width // 2, self.app.cell_height // 2))
        if len(path)==1:
            return path[0]
        else:
            return path[1]

    def move(self):
        self.direction = self.get_path_direction(self.app.target_point)

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + 25 + self.app.cell_width // 2,
                   (self.grid_pos[1] * self.app.cell_height) +
                   25 + self.app.cell_height // 2)

    def is_moving(self):
        if int(self.pix_pos.x + TOP_BOTTOM_PADDING // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_PADDING // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
