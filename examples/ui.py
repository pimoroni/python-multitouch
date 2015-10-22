import sys
import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
from gui import widgets, Button, Slider, Dial, fullscreen_message

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

def on_event(event, touch):
    for widget in widgets:
        widget.event(event, touch)

ts = Touchscreen()

for touch in ts.touches:
    touch.on_press = on_event
    touch.on_release = on_event
    touch.on_move = on_event

def button_event(b, e, t):
    print(b.label)


Dial(
    (0, 100),
    (255, 0, 0),
    (100, 380),
    80,
    None)

Dial(
    (0, 100),
    (255, 0, 0),
    (700, 380),
    80,
    None)

Button(
    "Quack!",
    (255, 0, 0),
    (20, 20),
    (160, 60), 
    button_event)

Button(
    "Duck!",
    (0,255,0), 
    (20, 100),
    (160, 60), 
    button_event)

Button(
    "Moo!",
    (0, 0, 255),
    (20, 180),
    (160, 60),
    button_event)

for x in range(6):
    Slider(
        (0,100),
        (255, 255, 0),
        (205 + (x*70), 20),
        (40, 390),
        None)

Slider(
    (0,100),
    (0, 255, 255),
    (205,430),
    (390,40),
    None)

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.flip()
                ts.stop()
                sys.exit()

    screen.fill((0, 0, 0))

    for widget in widgets:
        widget.render(screen)

    pygame.display.flip()

    time.sleep(0.01)
