import random
import math
from pico2d import *
import game_framework
import game_world
import layer
from life_gauge import LifeGauge
from score import ScoreObject

class Player:
    FIELD_MARGIN = 30
    RUN_SPEED_PPS = 300
    INITIAL_LIFE = 5
    image = None
    def __init__(self):
        if Player.image == None:
            Player.image = load_image('player.png')
        self.size = 60
        self.gauge = LifeGauge(570, 570, Player.INITIAL_LIFE, Player.INITIAL_LIFE)
        self.score = ScoreObject(50, 570)
        self.mouseControlled = False
        self.ready()


    def ready(self):
        self.x, self.y = get_canvas_width() / 2, get_canvas_height() / 2
        self.dx, self.dy = 0, 0
        self.speed = 1
        self.gauge.life = Player.INITIAL_LIFE
        self.score.score = 0

    def update(self):
        if game_world.isPaused:
            return
        dist = Player.RUN_SPEED_PPS * game_framework.frame_time
        if self.mouseControlled:
            mx, my = self.mouse_x - self.x, self.mouse_y - self.y
            angle = math.atan2(my, mx)
            if mx != 0 or my != 0:
                self.angle = angle
            dx, dy = math.cos(angle), math.sin(angle)
            tx, ty = self.x + (dx * dist), self.y + (dy * dist)
            if dx > 0 and tx > self.mouse_x: tx = self.mouse_x
            if dx < 0 and tx < self.mouse_x: tx = self.mouse_x
            if dy > 0 and ty > self.mouse_y: ty = self.mouse_y
            if dy < 0 and ty < self.mouse_y: ty = self.mouse_y
            self.x, self.y = tx, ty
        else:
            self.x += self.dx * dist
            self.y += self.dy * dist

        self.x = clamp(Player.FIELD_MARGIN, self.x, get_canvas_width() - Player.FIELD_MARGIN)
        self.y = clamp(Player.FIELD_MARGIN, self.y, get_canvas_height() - Player.FIELD_MARGIN)

        self.score.score += game_framework.frame_time

    def draw(self):
        self.image.draw(self.x, self.y)
        self.score.draw()
        self.gauge.draw()
    def decrease_life(self):
        self.gauge.life -= 1
        return self.gauge.life > 0
    def recover_life(self, item):
        if self.gauge.life < self.gauge.max:
            self.gauge.life += 1
        else:
            self.score.score += item.score
    def apply_pause_panalty(self):
        self.score.score = max(0, self.score.score - 2) #2씩 빼되 최소값은 0까지, 점수가 마이너스 안되도록
    def get_speed(self):
        return 1 + self.score.score / 60
    def get_max_obstacle(self):
        return 10 + self.score.score // 10

    def get_bb(self):
        return self.x - 10, self.y - 40, self.x + 15, self.y + 40

    def handleEvent(self, e):
        handled = False
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.dx -= self.speed
            elif e.key == SDLK_RIGHT:
                self.dx += self.speed
            elif e.key == SDLK_DOWN:
                self.dy -= self.speed
            elif e.key == SDLK_UP:
                self.dy += self.speed

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.dx += self.speed
            elif e.key == SDLK_RIGHT:
                self.dx -= self.speed
            elif e.key == SDLK_DOWN:
                self.dy += self.speed
            elif e.key == SDLK_UP:
                self.dy -= self.speed

        elif e.type == SDL_MOUSEBUTTONDOWN:
            self.mouseControlled = True
            handled = True

        if e.type in [SDL_MOUSEBUTTONDOWN, SDL_MOUSEMOTION]:
            self.mouse_x, self.mouse_y = e.x, get_canvas_height() - e.y

        if self.dx != 0 or self.dy != 0:
            self.mouseControlled = False
            handled = True

        return handled


