import random

import numpy as np
import pygame

from GraphAlgs import GraphAlgs
from enemy import Enemy
from player import Player
from utils import *


class GameState:
    def __init__(self, screen, app):
        self.screen = screen
        self.app = app
        self.running = True
        # pygame.sprite.Sprite.__init__(self)
        # self.cell_width = MAZE_WIDTH // 28
        # self.cell_height = MAZE_HEIGHT // 30
        # self.image = pygame.image.load('assets/stone.png').convert()
        # self.image = pygame.transform.scale(self.image, (self.cell_width, self.cell_height))
        # self.maze_array = np.array(self.getArray2d())
        # np.random.shuffle(self.maze_array)
        # self.transform_maze()
        # self.maze = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        # self.draw_maze()
        # self.walls = []
        # self.coins = []
        # self.enemies = []
        # self.p_pos = None
        # self.e_pos = []
        # self.load()



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


