import sys
import pygame
import time
import os
from pygame.locals import *
import ft5406

col = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (127, 127, 127),
    (127, 255, 127),
    (255, 127, 127),
    (255, 255, 127)
]

buttons = []

class Button:

    def __init__(self, color, x, y, w, h, action):
        global buttons
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.active = True
        self.action = action
        buttons.append(self)
        self.color =  color
        self.thickness = 2

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.position, self.size), 2)

    def collide(self, event, touch):
        if self.active:
            x, y = touch.position
            if x >= self.x and x <= self.x + self.w:
                if y >= self.y and y <= self.y + self.h:
                    if callable(self.action):
                        self.action(event, touch)
        return False

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def size(self):
        return (self.w, self.h)


pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

def on_press(event, touch):
    touch.last_x = touch._x
    touch.last_y = touch._y

    for button in buttons:
        button.collide(event, touch)

    pass

def on_release(event, touch):
    pass

def on_move(event, touch):
    #pygame.draw.line(
    #    screen,
    #    col[touch.slot],
    #    touch.last_position,
    #    touch.position)
    pass

ts = ft5406.Touchscreen()

for touch in ts.touches:
    touch.on_press = on_press
    touch.on_release = on_release
    touch.on_move = on_move

my_button = Button((255, 0, 0), 20, 20, 200, 50, 
    lambda e,t: print("Quack!",t.slot))

py_arr = Button((0,255,0), 20, 80, 200, 50, 
    lambda e,t: print("Duck!",t.slot))

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    for button in buttons:
        button.render(screen)

    pygame.display.flip()

    time.sleep(0.001)
