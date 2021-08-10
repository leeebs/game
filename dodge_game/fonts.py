from pico2d import *

fonts = {}

FONT_1 = 'segoepr.ttf'

def get(file, size):
    global fonts
    key = file + '_' + str(size)
    if key in fonts: 
        return fonts[key]

    font = load_font(file, size) 
    fonts[key] = font  
    return font  
