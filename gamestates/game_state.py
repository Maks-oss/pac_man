import pygame

from buttons import button
from enemy import Enemy
from player import Player
from utils import *


class GameState:
    def __init__(self, screen,app):
        self.screen = screen
        self.app = app
        self.running = True
        self.maze = pygame.transform.scale(pygame.image.load('assets/maze.png'), (MAZE_WIDTH, MAZE_HEIGHT))
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.walls = []
        self.coins = []
        self.enemies = []
        self.p_pos = None
        self.e_pos = []
        self.load()
        self.player = Player(self, self.p_pos)
        self.make_enemies()

    def load(self):
        with open('walls.txt', mode='r') as file:
            for xid, lines in enumerate(file):
                for yid, char in enumerate(lines):
                    if char == "1":
                        self.walls.append(vec(yid, xid))
                    elif char == "C":
                        self.coins.append(vec(yid, xid))
                    elif char == "P":
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
            self.enemies.append(Enemy(self, pos))
