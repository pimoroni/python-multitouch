import sys
import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE
from gui import Widget, Button, Dial, touchscreen_event, render_widgets

ship = [None,None]

class Ship(Widget):

    def __init__(self, color, position, velocity):
        self.vx, self.vy = velocity
        self.drag = 0.95
        self.thrust = False
        self.color = color

        super(Ship, self).__init__(position, (0, 0))

    def touch_inside(self, touch):
        pass

    def event(self, event, touch):
        pass

    def update(self):
        self.x = int(self.x + self.vx)
        self.y = int(self.y + self.vy)
    
        if not self.thrust:
            self.vx *= self.drag
            if abs(self.vx) <= 0.001:
                self.vx = 0
            self.vy *= self.drag
            if abs(self.vy) <= 0.001:
                self.vy = 0

        if self.x >= 800:
            self.x = 799

        if self.y >= 479:
            self.y = 479

        if self.x < 0:
            self.x = 0

        if self.y < 0:
            self.y = 0

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.position, 10, 0)

        text = self.font.render("v:{},{}".format(
            round(self.vx*10)/10.0,
            round(self.vy*10)/10),
             1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.x
        textpos.centery = self.y + 10
        screen.blit(text, textpos)


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

def update_ship_velocity(ship_idx, angle, velocity):
    global ship
    s = ship[ship_idx]
    velocity = min(1,velocity)

    if velocity == 0:
        s.thrust = False

    if s is not None and velocity > 0.1:
        s.thrust = True
        s.vx = velocity * 10 * math.cos(angle)
        s.vy = velocity * 10 * math.sin(angle)

Dial(
    (0, 100),
    (255, 0, 255),
    (100, 240),
    80,
    lambda v, a: update_ship_velocity(0, v, a))

Dial(
    (0, 100),
    (255, 255, 0),
    (700, 240),
    80,
    lambda v, a: update_ship_velocity(1, v, a))

Button(
    "X",
    (255, 0, 0),
    (760, 0),
    (40, 40),
    stop)

ship = [
    Ship((255, 0, 255),(400, 240),(0, 0)),
    Ship((255, 255, 0),(400, 250),(0, 0))]

ts.run()

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            ts.stop()
            sys.exit()

    for s in ship:
        s.update()

    screen.fill((0, 0, 0))

    render_widgets(screen)    

    pygame.display.flip()

    time.sleep(0.01)

ts.stop()
