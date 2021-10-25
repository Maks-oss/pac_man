import csv

import pygame

import gamestates.play_state as play_state
from buttons import button
from gamestates.game_state import GameState
from utils import WIDTH, BLACK, HEIGHT, RED


class GameOver(GameState):

    def __init__(self, screen, app, is_won, time, agent):
        super().__init__(screen, app)
        with open('results.csv', 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(["Win" if is_won else "Lose", time, agent])

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1.collidepoint(pygame.mouse.get_pos()):
                    self.app.state = play_state.Play(self.screen, self.app)
                elif self.button2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.screen, [WIDTH // 2, 100], 52, RED, "arial", centered=True)
        self.button1 = button(self.screen, (WIDTH // 2 - 50, WIDTH // 2), "Play again")
        self.button2 = button(self.screen, (WIDTH // 2 - 50, HEIGHT // 2 + 50), "Quit")
        pygame.display.update()
