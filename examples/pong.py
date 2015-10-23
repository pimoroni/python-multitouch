import sys
import pygame
import time
import os
from pygame.locals import *
import ft5406
from gui import text
from collections import namedtuple
import math

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = ft5406.Touchscreen()

Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')

def millis():
    return int(round(time.time() * 1000))

class Ball():
    def __init__(self):
        
        global width, height

        self.speed = 0.3
        self.angle = 0

        self.x = width/2
        self.y = height/2

        self.vx = self.speed*math.cos(self.angle)
        self.vy = self.speed*math.sin(self.angle)

        self.radius = 10

        self.color = (255, 255, 255)

    def intersects(self, rect):
        rx, ry = rect.center
        rw, rh = rect.size

        dist_x = abs(self.x - rx)
        dist_y = abs(self.y - ry)

        if dist_x > rw/2.0+self.radius or dist_y > rh/2.0+self.radius:
            return False

        if dist_x <= rw/2.0 or dist_y <= rh/2.0:
            return True

        cx = dist_x-rw/2.0
        cy = dist_y-rh/2.0

        c_sq = cx**2.0 + cy**2.0

        return c_sq <= self.radius**2.0

    def update(self, delta, collide):
        global width

        self.x += self.vx * delta
        self.y += self.vy * delta

        for item in collide:
            if self.intersects(item):
                cx, cy = item.center
                w, h = item.size

                relative_y = (cy - self.y) / (h/w)

                angle = relative_y * 5*(math.pi/12)

                self.vx = self.speed*math.cos(angle)
                self.vy = self.speed*math.sin(angle)


        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -1

        if self.y - self.radius <=0:
            self.y = self.radius
            self.vy *= -1

        if self.y + self.radius >= height:
            self.y = height - self.radius
            self.vy *= -1

        if self.x + self.radius >= width:
            self.x = width - self.radius
            self.vx *= -1

    @property
    def position(self):
        return Position(x=self.x, y=self.y)

    def render(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            [int(x) for x in self.position],
            self.radius,
            0)


class Player():
    def __init__(self, side):

        global width, height

        self.y = height/2
        self.next_y = self.y

        if side == 0: # Left
            self.x = 50
        else:
            self.x = width - 50
        
        self.width = 20
        self.height = 50

    def paddle(self, y):
        self.next_y = y

    @property
    def center(self):
        return Position(
            x=self.x,
            y=self.y)

    @property
    def position(self):
        return Position(
            x=self.x - (self.width/2),
            y=self.y - (self.height/2))

    @property
    def size(self):
        return Size(
            w=self.width,
            h=self.height)

    def update(self):
        self.y = self.next_y

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
ball = Ball()

touch_zone = 100

time_last = millis()

while True:
    time_now = millis()
    time_delta = time_now - time_last

    for touch in ts.poll():
        if not touch.valid:
            continue

        x, y = touch.position

        print("Got touch at {},{}".format(x, y))

        if x < 50:
            player_one.paddle(y)
        elif x > width-50:
            player_two.paddle(y)
                    

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    text(screen, "Hit ESC to exit!", (400, 460), 30, (255, 0, 0))  
    
    player_one.update()
    player_two.update()
    ball.update(time_delta,[player_one, player_two])

    ball.render(screen)
    player_one.render(screen)
    player_two.render(screen)

    pygame.display.flip()

    time.sleep(0.001)
    time_last = time_now
