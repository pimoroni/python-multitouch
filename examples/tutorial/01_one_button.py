import sys
sys.path.append('../')

import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen
from gui import Button, render_widgets, touch_widgets


pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = Touchscreen()

for touch in ts.touches:
    touch.on_press = touch_widgets
    touch.on_release = touch_widgets
    touch.on_move = touch_widgets

def button_event(b, e, t):
    print("{} pressed!".format(b.label))

Button(
    "My Button",
    (255, 0, 0),
    (300, 100),
    (200, 190), 
    button_event)

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.flip()
                ts.stop()
                sys.exit()

    screen.fill((0, 0, 0))

    render_widgets(screen)

    pygame.display.flip()

    time.sleep(0.01)
