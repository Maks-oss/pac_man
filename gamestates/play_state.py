import pygame
from pygame.math import Vector2 as vec

from gamestates.game_state import GameState
from gamestates.gameover_state import GameOver
from utils import BLACK


class Play(GameState):
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x * self.cell_width) + self.cell_width // 2 + 25,
                                int(coin.y * self.cell_height) + self.cell_height // 2 + 25), 5)

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.app.state = GameOver(self.screen, self.app)
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.maze, (25, 25))
        self.draw_text('Current score: {}'.format(self.player.current_score), self.screen, [60, 0], 18, (255, 255, 255),
                       'arial black')
        self.player.draw(self.screen)
        self.draw_coins()
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.update()

    def __init__(self, screen, app):
        super().__init__(screen, app)
