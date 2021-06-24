from pico2d import *
import images

class Background:
    def __init__(self):
        self.image_space = images.get('outerspace.png')
        self.image_stars = images.get('stars.png')
        self.space_point = 0, 0
        self.stars_point = 0, 0
        self.target = None
    def update(self):
        hw = get_canvas_width() // 2
        hh = get_canvas_height() // 2
        dx, dy = self.target.x - hw, self.target.y - hh  
        self.space_point = hw - 0.02 * dx, hh - 0.02 * dy
        self.stars_point = hw - 0.05 * dx, hh - 0.05 * dy
    def draw(self):
        self.image_space.draw(*self.space_point)
        self.image_stars.draw(*self.stars_point) #=self.stars_point[0], self.stars_point[0]
