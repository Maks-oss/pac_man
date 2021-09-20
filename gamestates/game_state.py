import random

import numpy as np
import pygame

from GraphAlgs import GraphAlgs
from enemy import Enemy
from player import Player
from utils import *


class GameState(pygame.sprite.Sprite):
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.running = True
        pygame.sprite.Sprite.__init__(self)
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.image = pygame.image.load('assets/stone.png').convert()
        self.image = pygame.transform.scale(self.image, (self.cell_width, self.cell_height))
        self.maze_array = np.array(self.getArray2d())
        np.random.shuffle(self.maze_array)
        self.transform_maze()
        self.maze = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        self.draw_maze()
        self.walls = []
        self.coins = []
        self.enemies = []
        self.p_pos = None
        self.e_pos = []
        self.load()
        self.set_point()
        self.player = Player(self, self.p_pos,self.app.target_point)
        self.graph_alg=GraphAlgs(self.walls)
        self.make_enemies()


    def set_point(self):
        rand_point = [random.randint(0, len(self.maze_array)-1), random.randint(0, len(self.maze_array[0])-1)]
        if self.maze_array[rand_point[0]][rand_point[1]] == 'C' and self.app.target_point is None:
            self.app.target_point = rand_point
            print("Random",rand_point)
        elif self.app.target_point is not None:
            return
        else:
            self.set_point()

    def transform_maze(self):
        for idx, x in enumerate(self.maze_array):
            if idx == 0 or idx == len(self.maze_array) - 1:
                self.maze_array[idx] = '1111111111111111111111111111'
            for jdx, y in enumerate(x):
                if jdx == 0 or jdx == len(self.maze_array[0]) - 1:
                    self.maze_array[idx] = self.maze_array[idx][:jdx] + '1' + self.maze_array[idx][jdx + 1:]
        if not any('P' in sublist for sublist in self.maze_array):
            self.maze_array[2] = self.maze_array[2][:2] + 'P' + self.maze_array[2][2:]

    def getArray2d(self):
        with open('walls.txt', mode='r') as file:
            return [row.rstrip('\n') for row in file.readlines()]

    def draw_maze(self):
        for xid, i in enumerate(self.maze_array):
            for yid, j in enumerate(i):
                if j == "1":
                    pygame.draw.rect(self.maze, BLUE, (yid * self.cell_width, xid * self.cell_height,
                                                       self.cell_width, self.cell_height))
                    # self.screen.blit(self.image, (yid * self.cell_width, xid * self.cell_height,
                    #                                    self.cell_width, self.cell_height))

    def load(self):
        for xid, lines in enumerate(self.maze_array):
            for yid, char in enumerate(lines):
                if char == "1":
                    self.walls.append(vec(yid, xid))
                elif char == "C":
                    self.coins.append(vec(yid, xid))
                elif char == "P":
                    # print("Char")
                    self.p_pos = [yid, xid]
                elif char in ["2", "3", "4", "5"]:
                    self.e_pos.append([yid, xid])
                elif char == "B":
                    pygame.draw.rect(self.maze, BLACK, (yid * self.cell_width, xid * self.cell_height,
                                                        self.cell_width, self.cell_height))

    def event(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            if idx == 0:
                self.enemies.append(Enemy(self, pos, RED))
            if idx == 1:
                self.enemies.append(Enemy(self, pos, BLUE_LIGHT))
            # if idx == 2:
            #     self.enemies.append(Enemy(self, pos, PLAYER_COLOUR))
            # if idx == 3:
            #     self.enemies.append(Enemy(self, pos, GREY))
