import pygame

from utils import *
import time
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos):
        self.app = app
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pac.png').convert()
        self.image = pygame.transform.scale(self.image, (self.app.cell_width, self.app.cell_height))
        self.grid_pos = pos
        self.old_path = []
        self.current_alg = 'DFS'
        self.current_time = 0
        self.previous_grid_pos = pos
        self.starting_pos = [pos[0], pos[1]]
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 1
        self.lives = 1

    def update(self):
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.is_moving():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        self.grid_pos[0] = (self.pix_pos[0] - 50 +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - 50 +
                            self.app.cell_height // 2) // self.app.cell_height + 1

        self.show_algorithm()
        if self.on_coin():
            self.eat_coin()

    def show_algorithm(self):
        if self.old_path:
            for p in self.old_path:
                pygame.draw.rect(self.app.maze, BLACK, p)
            self.old_path = []
        if self.current_alg == 'DFS':
            start = time.time()
            self.draw_dfs()
            end = time.time()
            self.current_time=end-start
        elif self.current_alg == 'BFS':
            start = time.time()
            self.draw_bfs()
            end = time.time()
            self.current_time=end-start

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

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def change_algorithm(self):
        if self.current_alg == 'DFS':
            self.current_alg = 'BFS'
        elif self.current_alg == 'BFS':
            self.current_alg = 'DFS'

    def move(self, direction):
        self.stored_direction = direction

    def draw_bfs(self):
        for enemy in self.app.enemies:
            for p in enemy.BFS(self.grid_pos, enemy.grid_pos):
                self.old_path.append((p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                      self.app.cell_width // 2, self.app.cell_height // 2))
                pygame.draw.rect(self.app.maze, enemy.color, (p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                                              self.app.cell_width // 2, self.app.cell_height // 2))

    def draw_dfs(self):
        for enemy in self.app.enemies:
            for p in enemy.DFS(self.grid_pos, enemy.grid_pos):
                self.old_path.append((p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                      self.app.cell_width // 2, self.app.cell_height // 2))
                pygame.draw.rect(self.app.maze, enemy.color, (p[0] * self.app.cell_width, p[1] * self.app.cell_height,
                                                              self.app.cell_width // 2, self.app.cell_height // 2))

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

    def can_move(self):

        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
