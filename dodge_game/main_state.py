# import pico2d
import random
from pico2d import *
import game_framework
import game_world
import layer
from player import Player
from missile import Missile
from background import Background
import images
from item import Item, CoinItem
from highscore import Highscore

player = None
gameOverImage = None
music_bg =None
wav_bomb =None
wav_item =None
highscore = None

GAMESTATE_READY, GAMESTATE_INPLAY, GAMESTATE_PAUSED, GAMESTATE_GAMEOVER = range(4)
gameState = GAMESTATE_READY

def generate_coords():
    field_width = get_canvas_width()
    field_height = get_canvas_height()

    dx, dy = random.random(), random.random()
    if dx < 0.5: dx -= 1 # (-1 ~ -0.5), (0.5 ~ 1.0)
    if dy < 0.5: dy -= 1 

    side = random.randint(1, 4) # 1=top, 2=left, 3=bottom, 4=right
    if side == 1: # top
        x, y = random.randint(0, field_width), field_height
        if dy > 0: dy = -dy
    elif side == 2: # left
        x, y = 0, random.randint(0, field_height)
        if dx < 0: dx = -dx
    elif side == 3: # bottom
        x, y = random.randint(0, field_width), 0
        if dy < 0: dy = -dy
    elif side == 4: # right
        x, y = field_width, random.randint(0, field_height)
        if dx > 0: dx = -dx

    global player
    speed = player.get_speed()
    dx, dy = dx * speed, dy * speed

    return x, y, dx, dy

def create_missile():
    (x, y, dx, dy) = generate_coords()
    size = random.randint(30, 60)
    m = Missile(x, y, dx, dy, size)
    game_world.add(m, layer.obstacle)

def create_item():
    (x, y, dx, dy) = generate_coords()
    if random.random() < 0.5:
        item = Item(x, y, dx, dy)
    else:
        item = CoinItem(x, y, dx, dy)
    game_world.add(item, layer.item)


def ready_game():
    global gameState
    gameState = GAMESTATE_READY
    game_world.isPaused = True
    game_world.clear_at_layer(layer.obstacle)
    game_world.clear_at_layer(layer.item)

    global player
    player.ready()

def start_game():
    global gameState
    gameState = GAMESTATE_INPLAY
    game_world.isPaused = False

    global music_bg
    music_bg.repeat_play()

def end_game():
    global gameState
    gameState = GAMESTATE_GAMEOVER
    game_world.isPaused = True

    global player, highscore
    highscore.add(player.score.score)

    global music_bg
    music_bg.stop()

def toggle_gamestate():
    global gameState, music_bg, player
    if gameState == GAMESTATE_INPLAY:
        gameState = GAMESTATE_PAUSED
        game_world.isPaused = True
        music_bg.pause()
        player.apply_pause_panalty()
    elif gameState == GAMESTATE_PAUSED:
        gameState = GAMESTATE_INPLAY
        game_world.isPaused = False
        music_bg.resume()


def collides_distance(a, b):
    dx, dy = a.x - b.x, a.y - b.y
    dist_sq = dx ** 2 + dy ** 2
    rsum_sq = (a.size / 2 + b.size / 2) ** 2
    return dist_sq < rsum_sq

def enter():
    game_world.init(layer.count)
    global player
    player = Player()
    game_world.add(player, layer.player)


    bg = Background()
    bg.target = player
    game_world.add(bg, layer.bg)



    global gameOverImage
    gameOverImage = images.get('game_over.png')

    global music_bg, wav_bomb, wav_item
    music_bg = load_music('background.mp3')
    music_bg.set_volume(64)
    wav_bomb = load_wav('explosion.wav')
    wav_item = load_wav('item.wav')

    global highscore
    highscore = Highscore()


    ready_game()

    # for i in range(10):
    #     create_missile()

def exit():
    global music_bg, wav_bomb, wav_item
    del music_bg, wav_bomb, wav_item

def update():
    global player
    game_world.update()
    global wav_bomb
    for m in game_world.objects_at_layer(layer.obstacle):
        if collides_distance(player, m):
            alive = player.decrease_life()
            if not alive:
                end_game()
            game_world.remove(m)
            wav_bomb.play()
            break
    global wav_item
    for m in game_world.objects_at_layer(layer.item):
        if collides_distance(player, m):
            player.recover_life(m)
            game_world.remove(m)
            wav_item.play()
            break

    cnt = game_world.count_at_layer(layer.obstacle)
    if cnt < player.get_max_obstacle():
        create_missile()
    # print('Missile count=', cnt)

    global gameState
    if gameState == GAMESTATE_INPLAY and random.random() < 0.01:
        create_item()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.draw()
    global gameState, highscore
    if gameState == GAMESTATE_GAMEOVER:
        gameOverImage.draw(400, 300)
        highscore.draw()
    update_canvas()

def handle_events():
    global player, gameState
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                game_framework.pop_state()
            elif e.key == SDLK_SPACE:
                toggle_gamestate()
            elif e.key == SDLK_RETURN:
                gameState == GAMESTATE_GAMEOVER
                ready_game()


        handled = player.handleEvent(e)
        if handled:
            if gameState == GAMESTATE_READY:
                start_game()
            if gameState == GAMESTATE_PAUSED:
                toggle_gamestate()
                #gameState = GAMESTATE_INPLAY
                #game_world.isPaused = False

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
