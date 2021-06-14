import random
from pico2d import *
import game_framework
import game_world
import layer
import images

class Item:
    RUN_SPEED_PPS = 200
    def __init__(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.size = 40
        self.score = 5
        self.image = images.get('present_box.png')
    def update(self):
        if game_world.isPaused:
            return
        dist = Item.RUN_SPEED_PPS * game_framework.frame_time
        self.x += self.dx * dist
        self.y += self.dy * dist
        if self.x < -self.size or \
          self.y < -self.size or \
          self.x > get_canvas_width() + self.size or \
          self.y > get_canvas_height() + self.size:
            game_world.remove(self)
    def draw(self):
        self.image.draw(self.x, self.y, self.size, self.size)

class CoinItem:
    def __init__(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.size = 30
        self.fps = 8
        self.fcount = 6
        self.time = 0
        self.score = 7.5
        self.frame = 0
        self.image = images.get('coin.png')
    def update(self):
        self.time += game_framework.frame_time
        self.frame = round(self.time * self.fps) % self.fcount
        Item.update(self)
    def draw(self):
        w = self.image.w //self.fcount
        h = self.image.h
        rect = (w * self.frame, 0, w, h)
        self.image.clip_draw(*rect, self.x, self.y, self.size, self.size)



