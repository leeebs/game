from pico2d import *
# import game_framework

# (LAYER_BG, LAYER_BALL, LAYER_PLAYER, LA..fjsdlk fsjlsf) = range(3)
# objects = [[],[],[],[]]
objects = []

def init(layer_count):
	global objects
	objects = []
	for i in range(layer_count):
		objects.append([])
	# print("Now layer count=", len(objects))

def add(obj, layer):
	global objects
	# print("in add(), layer count=", len(objects))
	objects[layer].append(obj)

def remove(obj):
	global objects
	for i in range(len(objects)):
		if obj in objects[i]:
			objects[i].remove(obj)
			del obj
			break

def objects_at_layer(layer):
	for o in objects[layer]:
		yield o

def count_at_layer(layer):
	global objects
	return len(objects[layer])

def clear():
	global objects
	for i in range(len(objects)):
		for obj in objects[i]:
			del obj
	objects = []

def clear_at_layer(layer):
	global objects
	for obj in objects[layer]:
		del obj
	objects[layer] = []

def update():
	for i in range(len(objects)):
		for obj in objects[i]:
			obj.update()

def draw():
	for i in range(len(objects)):
		for obj in objects[i]:
			obj.draw()
