import sys
import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen
from gui import widgets, Button, Slider, Dial, render_widgets, touchscreen_event

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = Touchscreen()

for touch in ts.touches:
    touch.on_press = touchscreen_event
    touch.on_release = touchscreen_event
    touch.on_move = touchscreen_event

def button_event(b, e, t):
    print(b.label)

def my_exit(b, e, t):
    global running
    running = False

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

Button(
    "x",
    (255, 0, 0),
    (760, 0),
    (40, 40),
    my_exit)

for x in range(6):
    Slider(
        (0,100,0),
        (255, 255, 0),
        (205 + (x*70), 20),
        (40, 390),
        None)

Slider(
    (0,100,0),
    (0, 255, 255),
    (205,430),
    (390,40),
    None)

ts.run()

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            ts.stop()
            sys.exit()

    screen.fill((0, 0, 0))

    render_widgets(screen)

    pygame.display.flip()

    time.sleep(0.01)

ts.stop()
