import pygame
import random

from utils import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        self.app = app
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/blinky.png').convert()
        self.image=pygame.transform.scale(self.image, (self.app.cell_width , self.app.cell_height ))
        self.grid_pos = pos
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width // 2.3)
        self.direction = vec(0, 0)
        self.target = None
        self.speed = 2

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.time_to_move():
                self.move()

        self.grid_pos[0] = (self.pix_pos[0] - 50 +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - 50 +
                            self.app.cell_height // 2) // self.app.cell_height + 1

    def draw(self,screen):
        screen.blit(self.image, (self.pix_pos.x-10,
                                 self.pix_pos.y-10))

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
        self.direction = self.get_random_direction()

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
