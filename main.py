import sys

from gamestates.game_state import *
from gamestates.intro_state import Intro

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = Intro(self.screen,self)

    def run(self):
        while self.state.running:
            self.state.draw()
            self.state.event()
            self.state.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()
