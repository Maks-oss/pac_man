import csv
import sys

import pandas as pd
from sklearn.linear_model import LinearRegression

from gamestates.game_state import *
from gamestates.intro_state import Intro
from utils import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.state = Intro(self.screen, self)

    def run(self):
        while self.state.running:
            self.state.draw()
            self.state.event()
            self.state.update()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


def analyze():
    data = pd.read_csv('results.csv')
    X = data.iloc[:, 0:2].values
    Y = data.iloc[:, 2:].values.reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)
    with open('results_predict.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(["Won", "Score"])
        for i in Y_pred:
            for j in i:
                writer.writerow([0 if round(j) < 70 else 1, round(j)])


if __name__ == '__main__':
    app = App()
    analyze()
    # app.run()
