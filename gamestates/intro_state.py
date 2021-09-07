import pygame

from buttons import button
from gamestates.game_state import GameState
from gamestates.play_state import Play
from utils import WIDTH, HEIGHT


class Intro(GameState):
    def __init__(self, screen,app):
        super().__init__(screen,app)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1.collidepoint(pygame.mouse.get_pos()):
                    self.app.state = Play(self.screen,self.app)
                elif self.button2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text('PAC MAN', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 100], 36, (170, 132, 58), 'arial black', centered=True)
        self.button1 = button(self.screen, (WIDTH // 2 - 50, WIDTH // 2), "Start game")
        self.button2 = button(self.screen, (WIDTH // 2 - 50, HEIGHT // 2 + 50), "Quit game")
        pygame.display.update()