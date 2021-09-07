import sys

import pygame

from buttons import button
from utils import *
from player import Player

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):

        self.state = None
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'
        self.maze = pygame.transform.scale(pygame.image.load('maze2.png'), (MAZE_WIDTH, MAZE_HEIGHT))
        self.cell_width = MAZE_WIDTH // 28
        self.cell_height = MAZE_HEIGHT // 30
        self.walls=[]
        self.coins=[]
        self.load()

        self.player = Player(self, vec(1, 1))

    def load(self):
        with open('walls.txt',mode='r') as file:
            for xid,lines in enumerate(file):
                for yid,char in enumerate(lines):
                    if char=="1":
                        self.walls.append(vec(yid,xid))
                    elif char=="C":
                        self.coins.append(vec(yid,xid))

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
            self.clock.tick(60)
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

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7),
                               (int(coin.x*self.cell_width)+self.cell_width//2+25,
                                int(coin.y*self.cell_height)+self.cell_height//2+25), 5)

    def intro_draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_text('PAC MAN', self.screen, [
            WIDTH // 2, HEIGHT // 2 - 100], 36, (170, 132, 58), 'arial black', centered=True)
        self.button1 = button(self.screen, (WIDTH // 2 - 50, WIDTH // 2), "Start game")
        self.button2 = button(self.screen, (WIDTH // 2 - 50, HEIGHT // 2 + 50), "Quit game")
        pygame.display.update()

    def play_events(self):
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

    def play_update(self):
        self.player.update()

    def play_draw(self):
        self.screen.blit(self.maze, (25, 25))
        # self.draw_grid()
        print(self.player.current_score)
        self.draw_text('Current score: {}'.format(self.player.current_score), self.screen, [10, 0], 18, (255, 255, 255),'arial black')
        self.player.draw()
        self.draw_coins()
        pygame.display.update()

    def draw_grid(self):

        for x in range(WIDTH // self.cell_width + 1):
            pygame.draw.line(self.maze, (136, 136, 136), (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_width):
            pygame.draw.line(self.maze, (136, 136, 136), (0, x * self.cell_height), (WIDTH, x * self.cell_height))
        # for wall in self.walls:
        #     pygame.draw.rect(self.maze,(112,55,163),(wall.x*self.cell_width,wall.y*self.cell_height,self.cell_width,self.cell_height))

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
