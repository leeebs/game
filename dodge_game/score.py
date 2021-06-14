import random
from pico2d import *
import game_framework
import game_world
import layer
import fonts

class ScoreObject:
    font = None
    def __init__(self, x, y):
        self.font = fonts.get(fonts.FONT_1, 50)
        self.score = 0
        self.x, self.y = x, y
        self.color = (170, 240, 209)
    def update(self):
        pass
    def draw(self):
        text = 'score: {:4.1f}'.format(self.score)
        self.font.draw(self.x, self.y, text, self.color)