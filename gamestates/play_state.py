import random
import time

import numpy as np
import pygame

from algs.GraphAlgs import GraphAlgs
from enemy import Enemy
from gamestates.game_state import GameState
from gamestates.gameover_state import GameOver
from player import Player
from utils import *


class Play(GameState):
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_z:
                #     self.player.change_algorithm()
                if event.key == pygame.K_x:
                    self.player.change_agent()

    def update(self):
        self.player.update()
        if self.player.current_score == 70:
            self.app.state = GameOver(self.screen, self.app, is_won=True, time=(time.time() - self.timer),
                                      score=self.player.current_score,
                                      )
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()
        # for enemy in self.enemies:
        #     for p in enemy.BFS(enemy.grid_pos,self.player.grid_pos):
        #         pygame.draw.rect(self.maze, enemy.color, (p[0] * self.cell_width, p[1] * self.cell_height,
        #                                           self.cell_width//2, self.cell_height//2))

    def draw_bfs(self):
        for enemy in self.enemies:
            for p in enemy.BFS(enemy.grid_pos, self.player.grid_pos):
                pygame.draw.rect(self.maze, enemy.type, (p[0] * self.cell_width, p[1] * self.cell_height,
                                                         self.cell_width // 2, self.cell_height // 2))

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin[0] * self.cell_width) + self.cell_width // 2 + 25,
                                int(coin[1] * self.cell_height) + self.cell_height // 2 + 25), 5)

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.app.state = GameOver(self.screen, self.app, is_won=False, time=(time.time() - self.timer),
                                      score=self.player.current_score,
                                      )
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

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
        with open('walls2.txt', mode='r') as file:
            return [row.rstrip('\n') for row in file.readlines()]

    def draw_maze(self):
        for xid, i in enumerate(self.maze_array):
            for yid, j in enumerate(i):
                if j == "1":
                    pygame.draw.rect(self.maze, BLUE, (yid * self.cell_width, xid * self.cell_height,
                                                       self.cell_width, self.cell_height))
                elif j == 'P':
                    pygame.draw.rect(self.maze, BLACK, (yid * self.cell_width, xid * self.cell_height,
                                                        self.cell_width, self.cell_height))

    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            # if idx == 0:
            #     self.enemies.append(Enemy(self, pos, 'random'))
            # if idx == 1:
            self.enemies.append(Enemy(self, pos, 'speed'))
        # if idx == 2:
        #     self.enemies.append(Enemy(self, pos, PLAYER_COLOUR))
        # if idx == 3:
        #     self.enemies.append(Enemy(self, pos, GREY))

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

    def set_point(self):
        rand_point = [random.randint(0, len(self.maze_array) - 1), random.randint(0, len(self.maze_array[0]) - 1)]
        if self.maze_array[rand_point[0]][rand_point[1]] == 'C':
            if self.graph_alg.UCS([int(self.p_pos[0]), int(self.p_pos[1])], [
                int(rand_point[0]), int(rand_point[1])]) is None:
                self.set_point()
            else:
                self.target_point = rand_point
                print("Random", rand_point)
                print("Pos", self.maze_array[self.target_point[0]][self.target_point[1]])
                return
        else:
            self.set_point()

    def set_agent(self, agent):
        rand_point = [random.randint(0, len(self.maze_array) - 1), random.randint(0, len(self.maze_array[0]) - 1)]
        if self.maze_array[rand_point[0]][rand_point[1]] == 'C':
            self.maze_array[rand_point[0]] = self.maze_array[rand_point[0]][:rand_point[1]] + agent + self.maze_array[
                                                                                                          rand_point[
                                                                                                              0]][
                                                                                                      rand_point[
                                                                                                          1] + 1:]
        else:
            self.set_agent(agent)

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.maze, (25, 25))
        self.draw_text('Current score: {}'.format(self.player.current_score), self.screen, [60, 0], 18, (255, 255, 255),
                       'arial black')
        self.draw_text('Current agent: {}'.format(self.player.current_agent), self.screen, [300, 0], 18,
                       (255, 255, 255),
                       'arial black')
        self.player.draw(self.screen)
        self.draw_coins()
        self.draw_point()
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.update()

    def draw_point(self):
        pygame.draw.circle(self.screen, RED,
                           (int(self.target_point[0] * self.cell_width) + self.cell_width // 2 + 25,
                            int(self.target_point[1] * self.cell_height) + self.cell_height // 2 + 25), 8)

    # def generate_newstate(self):
    #

    def __init__(self, screen, app):
        super().__init__(screen, app)
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.image = pygame.image.load('assets/stone.png').convert()
        self.image = pygame.transform.scale(self.image, (self.cell_width, self.cell_height))
        self.maze_array = np.array(self.getArray2d())
        self.set_agent('P')
        self.set_agent('2')
        self.set_agent('3')
        # np.random.shuffle(self.maze_array)
        # self.transform_maze()
        self.maze = pygame.Surface((MAZE_WIDTH, MAZE_HEIGHT))
        self.draw_maze()
        self.walls = []
        self.coins = []
        self.enemies = []
        self.p_pos = None
        self.is_win = False
        self.is_lose = False
        self.e_pos = []
        self.load()
        self.target_point = None
        self.graph_alg = GraphAlgs(self.walls)
        self.set_point()
        self.player = Player(self, self.p_pos)
        self.make_enemies()
        self.timer = time.time()
