import sys
import pygame
import time
import os
from pygame.locals import *
import ft5406
from gui import text

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = ft5406.Touchscreen()

start = [(0, 0) for x in range(10)]
state = [False for x in range(10)]
position = [(0,0) for x in range(10)]

while True:
    for touch in ts.poll():
        position[touch.slot] = (touch.x, touch.y)
        if state[touch.slot] != touch.valid:
            if touch.valid:
                print("{} pressed!".format(touch.slot))
                start[touch.slot] = (touch.x, touch.y)
            else:
                print("{} released!".format(touch.slot))
            state[touch.slot] = touch.valid

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    for x in range(10):
        if state[x]:
            pygame.draw.line(screen, (0, 0, 255), start[x], position[x])

    text(screen, "Hit ESC to exit!", (400, 460), 30, (255, 0, 0))  
    
    pygame.display.flip()

    time.sleep(0.001)
