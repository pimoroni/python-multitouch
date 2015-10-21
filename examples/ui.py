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

    def __init__(self, label, color, position, size, action):
        global buttons
        self.x, self.y = position
        self.w, self.h = size

        self.label = label

        self.active = True
        self.action = action
        buttons.append(self)
        self.color =  color
        self.thickness = 2

        self.font = pygame.font.Font(None, 30)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.position, self.size), 2)
        text = self.font.render(self.label, 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.x + (self.w/2)
        textpos.centery = self.y + (self.h/2)
        screen.blit(text, textpos)

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

def on_release(event, touch):
    pass

def on_move(event, touch):
    pass

ts = ft5406.Touchscreen()

for touch in ts.touches:
    touch.on_press = on_press
    touch.on_release = on_release
    touch.on_move = on_move

Button(
    "Quack!",
    (255, 0, 0),
    (20, 20),
    (200, 60), 
    lambda e,t: print("Quack!",t.slot))

Button(
    "Duck!",
    (0,255,0), 
    (20, 100),
    (200, 60), 
    lambda e,t: print("Duck!",t.slot))

Button(
    "Moo!",
    (0, 0, 255),
    (20, 180),
    (200, 60),
    lambda e,t: print("Moo!",t.slot))

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ts.stop()
                sys.exit()

    for button in buttons:
        button.render(screen)

    pygame.display.flip()

    time.sleep(0.001)
