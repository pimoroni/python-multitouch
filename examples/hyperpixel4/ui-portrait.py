import sys
import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen
from gui import widgets, Button, Slider, Dial, render_widgets, touchscreen_event

pygame.init()

size = width, height = 480, 800
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = Touchscreen(device="Goodix Capacitive TouchScreen")

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
    (100, 700),
    80,
    None)

Dial(
    (0, 100),
    (255, 0, 0),
    (380, 700),
    80,
    None)

Button(
    "Quack!",
    (255, 0, 0),
    (20, 530),
    (130, 60), 
    button_event)

Button(
    "Duck!",
    (0,255,0), 
    (175, 530),
    (130, 60), 
    button_event)

Button(
    "Moo!",
    (0, 0, 255),
    (330, 530),
    (130, 60),
    button_event)

Button(
    "x",
    (255, 0, 0),
    (440, 0),
    (40, 40),
    my_exit)

for x in range(6):
    Slider(
        (0,100,0),
        (255, 255, 0),
        (20 + (x*80), 60),
        (40, 390),
        None)

Slider(
    (0,100,0),
    (0, 255, 255),
    (20, 470),
    (440, 40),
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
