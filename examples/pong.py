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

class Player():
    def __init__(self, side):

        global width, height

        self.y = height/2

        if side == 0: # Left
            self.x = 50
        else:
            self.x = width - 50
        
        self.width = 20
        self.height = 50

    def paddle(self, y):
        self.y = y

    def render(self, screen):
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (
                (
                self.x - (self.width/2),
                self.y - (self.height/2)
                ),
                (
                self.width,
                self.height)
            ),
            0)

player_one = Player(0)
player_two = Player(1)

while True:
    for touch in ts.poll():
        if not touch.valid:
            continue

        x, y = touch.position

        print("Got touch at {},{}".format(x, y))
        
        if x < 400:
            player_one.paddle(y)
        else:
            player_two.paddle(y)
                    

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    text(screen, "Hit ESC to exit!", (400, 460), 30, (255, 0, 0))  

    player_one.render(screen)
    player_two.render(screen)

    pygame.display.flip()

    time.sleep(0.001)
