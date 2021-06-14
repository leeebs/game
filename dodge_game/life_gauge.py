import random
from pico2d import *
import game_framework
import game_world
import layer

class LifeGauge:
	red = None
	white = None
	def __init__(self, x, y, life, maxlife):
		if LifeGauge.red == None: LifeGauge.red = load_image('heart_red.png')
		if LifeGauge.white == None: LifeGauge.white = load_image('heart_white.png')
		self.x, self.y = x, y
		self.life = life
		self.max = maxlife
	def update(self):
		pass
	def draw(self):
		x, y = self.x, self.y
		for i in range(self.max):
			heart = LifeGauge.red if i < self.life else LifeGauge.white
			heart.draw(x, y)
			x += heart.w