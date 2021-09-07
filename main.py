import sys
from utils import *
import pygame

from buttons import button

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):

        self.state = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'
        self.maze = pygame.transform.scale(pygame.image.load('maze2.png'), (WIDTH, HEIGHT))
        self.cell_width=WIDTH//28
        self.cell_height=HEIGHT//30



    def run(self):
        while self.running:
            if self.state == 'intro':
                self.intro_draw()
                self.intro_events()
                self.intro_update()
            elif self.state == 'playing':
                self.play_events()
                self.play_update()
                self.play_draw()
            else:
                self.running = False
            # self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1.collidepoint(pygame.mouse.get_pos()):
                    self.state = 'playing'
                elif self.button2.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
            if event.type == pygame.QUIT:
                self.running = False

    def intro_update(self):
        pass

    def intro_draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text('PAC MAN', self.screen, [
            WIDTH//2, HEIGHT//2-100], 36, (170, 132, 58), 'arial black', centered=True)
        self.button1 = button(self.screen, (WIDTH//2-50, WIDTH//2), "Start game")
        self.button2 = button(self.screen, (WIDTH//2-50, HEIGHT//2+50), "Quit game")
        pygame.display.update()

    def play_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def play_update(self):
        pass

    def play_draw(self):
        self.screen.blit(self.maze, (0, 0))
        self.draw_grid()
        pygame.display.update()

    def draw_grid(self):
        print(self.cell_width,self.cell_height)
        for x in range(WIDTH//self.cell_width+1):
            pygame.draw.line(self.screen,(136,136,136),(x*self.cell_width,0),(x*self.cell_width,HEIGHT))
        for x in range(HEIGHT//self.cell_width):
            pygame.draw.line(self.screen,(136,136,136),(0,x*self.cell_height),(WIDTH,x*self.cell_height))

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)


if __name__ == '__main__':
    app = App()
    app.run()
