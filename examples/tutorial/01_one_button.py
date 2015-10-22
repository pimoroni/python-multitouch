import time
import pygame
from pygame.locals import *
from ft5406 import Touchscreen
from gui import Button, render_widgets, touchscreen_event

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
    print("{} pressed!".format(b.label))

Button(
    "My Button",
    (255, 0, 0),
    (300, 190),
    (200, 100), 
    button_event)

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
                ts.stop()
                exit()

    screen.fill((0, 0, 0))

    render_widgets(screen)

    pygame.display.flip()

    time.sleep(0.01)
