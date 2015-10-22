import sys
import pygame
import explorerhat
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

def stop(b, e, t):
    global running
    running = False

ts.run()

left = 0

def setup_light(idx, light):
    Button(
        light.name,
        [(0, 0, 255),(255, 255, 0),(255, 0, 0),(0, 255, 0)][x],
        (10 + left, 10),
        (100, 100),
        lambda b,e,t: light.toggle())
    
    Slider(
        (0,100,0),
        [(0, 0, 255),(255, 255, 0),(255, 0, 0),(0, 255, 0)][x],
        (10 + left, 120),
        (100, 350),
        lambda s,v: light.brightness(v))

        
for x in range(len(explorerhat.light)):
    light = explorerhat.light[x]
    setup_light(x, light)
    left += 110


Slider(
    (-100,100,0),
    (255,255,255),
    (450,10),
    (50, 460),
    lambda s, v:explorerhat.motor.one.speed(int(v)))

Slider(
    (-100,100,0),
    (255,255,255),
    (510,10),
    (50,460),
    lambda s, v:explorerhat.motor.two.speed(int(v)))

Button(
    "X",
    (255, 0, 0),
    (750, 10),
    (40, 40),
    stop)

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
