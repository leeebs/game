# import pico2d
# import random
from pico2d import *
import game_framework
# import font as font_mod



def enter():
    pass

def exit():
    pass

def update():
    pass

def draw():
    pass

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()

def pause():
    pass

def resume():
    pass


if __name__ == '__main__':
    import sys
    current_module = sys.modules[__name__]
    open_canvas()
    game_framework.run(current_module)
    close_canvas()
