from pico2d import *

images = {}


def get(file):
    global images
    if file in images:
        return images[file]

    image = load_image(file)
    images[file] = image
    return image