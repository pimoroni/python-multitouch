import sys
import random
import pygame
import time
import os
from pygame.locals import *
import ft5406
from gui import text
from collections import namedtuple
import math
from turtle import Vec2D

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

ts = ft5406.Touchscreen()

Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')

def millis():
    return int(round(time.time() * 1000))

def text(screen, text, position, size, color):
    font = pygame.font.SysFont("droidsansmono", size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx, textpos.centery = position
    screen.blit(text, textpos)

class Ball():
    def __init__(self):
        
        global width, height

        self.position = Vec2D(width/2, height/2)

        self.velocity = Vec2D(0.3,0.3)

        self.radius = 10

        self.color = (255, 255, 255)

    def reset(self):
        self.velocity = Vec2D(0.3,0.3).rotate(random.randint(0, 360))
        self.position = Vec2D(width/2, height/2)

    @property
    def x(self):
        return self.position[0]

    @x.setter
    def x(self, value):
        self.position = Vec2D(value, self.position[1])
    
    @property
    def y(self):
        return self.position[1]

    @y.setter
    def y(self, value):
        self.position = Vec2D(self.position[0], value)

    @property
    def vx(self):
        return self.velocity[0]

    @vx.setter
    def vx(self, value):
        self.velocity = Vec2D(value, self.velocity[1])

    @property
    def vy(self):
        return self.velocity[1]

    @vy.setter
    def vy(self, value):
        self.velocity = Vec2D(self.velocity[0], value)

    @property
    def speed(self):
        return abs(self.velocity)

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

    def update(self, delta, left_player, right_player):
        global width

        self.position += self.velocity * delta

        if (self.x < 100 and self.vx < 0) or (self.x > width - 100 and self.vx > 0):
            for item in [left_player, right_player]:
                if self.intersects(item):
                    item.success()

                    cx, cy = item.center
                    w, h = item.size
                    relative_y = (cy - self.y) / (h / 2)

                    speed = self.speed + (abs(relative_y)/4)

                    angle = relative_y * 5 * (math.pi / 12)
                    
                    if self.x > width/2:
                        self.x = item.position.x - self.radius 
                        self.velocity = Vec2D(
                            speed * -math.cos(angle),
                            speed * -math.sin(angle))
                    else:
                        self.x = item.position.x + item.width + self.radius
                        self.velocity = Vec2D(
                            speed * math.cos(angle),
                            speed * -math.sin(angle))


        if self.x - self.radius < 0 and self.vx < 0:
            left_player.fail()
            self.reset()
        elif self.x + self.radius > width and self.vx > 0:
            right_player.fail()
            self.reset()

        if self.y - self.radius < 0 and self.vy < 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius > height and self.vy > 0:
            self.y = height - self.radius
            self.vy *= -1


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
        
        self.score = 0
        self.y = height/2
        self.next_y = self.y

        if side == 0: # Left
            self.x = 50
        else:
            self.x = width - 50
        
        self.width = 10
        self.height = 100

    def paddle(self, y):
        self.next_y = y

    def success(self):
        self.score += 1

    def fail(self):
        self.score -= 1

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

        if x < touch_zone:
            player_one.paddle(y)
        elif x > width-touch_zone:
            player_two.paddle(y)
                    

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()

    screen.fill((0, 0, 0))

    text(screen, "Hit ESC to exit!", (400, 460), 30, (255, 0, 0))  

    pygame.draw.rect(
            screen,
            (64, 64, 64),
            (((width/2) - 2, 40),
            (4,height-80)),
            0
        )

    text(screen, "{0:02d}".format(player_one.score), (50, 50), 30, (255, 255, 255))
    text(screen, "{0:02d}".format(player_two.score), (width-50, 50), 30, (255, 255, 255))
    
    player_one.update()
    player_two.update()
    ball.update(time_delta, player_one, player_two)

    ball.render(screen)
    player_one.render(screen)
    player_two.render(screen)

    pygame.display.flip()

    time.sleep(0.001)
    time_last = time_now
