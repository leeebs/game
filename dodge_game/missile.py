import random
from pico2d import *
import game_framework
import game_world
import layer

class Missile:
    RUN_SPEED_PPS = 200
    image = None
    def __init__(self, x, y, dx, dy, size):
        if Missile.image == None:
            Missile.image = load_image('fireball.png')
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.size = size
        self.time = 0
        self.frame = 0
        self.fps = random.randint(2, 20)
        self.fcount = 24

    def update(self):
        self.time += game_framework.frame_time
        self.frame = round(self.time * self.fps) % self.fcount
        if game_world.isPaused:
            return
        dist = Missile.RUN_SPEED_PPS * game_framework.frame_time
        self.x += self.dx * dist
        self.y += self.dy * dist
        if self.x < -self.size or \
          self.y < -self.size or \
          self.x > get_canvas_width() + self.size or \
          self.y > get_canvas_height() + self.size:
            game_world.remove(self)
    def draw(self):
        # self.image.draw(self.x, self.y, self.size, self.size)
        self.image.clip_draw(128 * self.frame, 0, 128, 128, self.x, self.y, 2 * self.size, 2 * self.size)

    def get_bb(self):
        return self.x - 10, self.y - 40, self.x + 15, self.y + 40


