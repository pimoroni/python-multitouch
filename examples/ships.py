import sys
import pygame
import time
import os
import math
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

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

ship = [None,None]

widgets = []

class Widget:
    
    def __init__(self, position, size):
        global widgets

        try:
            callable(self.on_press)
        except AttributeError:
            self.on_press = None

        try:
            callable(self.on_release)
        except AttributeError:
            self.on_release = None

        try:
            callable(self.on_move)
        except AttributeError:
            self.on_move = None

        self.font = pygame.font.Font(None, 30)

        self.x, self.y = position
        self.w, self.h = size

        self.touches = []

        self.active = True
        
        widgets.append(self)

    def render(self):
        pass

    def touch_inside(self, touch):
        x, y = touch.position
        if x >= self.x and x <= self.x + self.w:
            if y >= self.y and y <= self.y + self.h:
                return True
        return False

    def event(self, event, touch):
        """Handle touch event"""

        """Handle pressing a widget

        A press can only be registered when it is in
        the widget bounds
        """
        if  self.touch_inside(touch):
            if event == TS_PRESS and touch not in self.touches:
                print("Appending touch {}".format(touch.slot))
                self.touches.append(touch)
                if self.active and callable(self.on_press):
                      self.on_press(event, touch)

        """Handle released touches.

        A touch can be released even when its not over a widget.
        """
        if event == TS_RELEASE and touch in self.touches:
            print("Removing touch {}".format(touch.slot))
            self.touches.remove(touch)
            if self.active and callable(self.on_release):
                self.on_release(event, touch)

        """Handle moving touches.

        Touch movement is tracked even when it's not over a widget
        """
        if event == TS_MOVE and touch in self.touches:
            print("Tracking touch {} {},{}".format(touch.slot,touch.x,touch.y))
            if self.active and callable(self.on_move):
                self.on_move(event, touch)

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def size(self):
        return (self.w, self.h)


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

        

class Dial(Widget):
    
    def __init__(self, min_max, color, position, radius, on_change):
        self.min_val, self.max_val = (min_max)
        self.color = color
        self.radius = radius
        self.distance = 0

        self._value_changed = on_change

        self.value = 0

        super(Dial, self).__init__(position, (radius, radius))

    def on_release(self, event, touch):
        self.distance = 0
        self.value = 0
        
        if callable(self._value_changed):
            self._value_changed(0, 0)

    def on_move(self, event, touch):
        if len(self.touches) > 1:
            return

        x, y = touch.position

        self.distance = math.hypot(x - self.x, y - self.y) / float(self.radius)
        
        #self.distance = math.sqrt((x - self.x)**2 + (y - self.y)**2) / float(self.radius)

        dx = x - self.x
        dy = y - self.y
    
        self.value = math.degrees(math.atan2(dy, dx) % (2*math.pi)) / 360.0

        if callable(self._value_changed):
            self._value_changed(self.value * 2 * math.pi, self.distance)


    def touch_inside(self, touch):
        x, y = touch.position
        #distance = math.hypot(x - self.x, y - self.y)

        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)

        if distance <= self.radius:
            return True

        return False

    def render(self, screen):
        thickness = 2
        pygame.draw.circle(screen, self.color, self.position, self.radius, thickness)

        
        handle_pos = (
            int(self.x + (self.radius * math.cos(self.value*2*math.pi))),
            int(self.y + (self.radius * math.sin(self.value*2*math.pi))))
    
        pygame.draw.circle(screen, self.color, handle_pos, thickness*3, thickness)

        text = self.font.render(str(int(self.value * 100)) + '%', 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.x
        textpos.centery = self.y
        screen.blit(text, textpos)
       
        text = self.font.render(str(int(self.distance * 100)) + '%', 1, self.color)
        textpos = text.get_rect()
        textpos.centerx, textpos.centery = handle_pos
        textpos.centery += 20
        screen.blit(text, textpos)

class Slider(Widget):

    def __init__(self, min_max, color, position, size, on_change):
        self.min_val, self.max_val = (min_max)
        self.color = color

        self._value_changed = on_change
        
        self.value = 0

        super(Slider, self).__init__(position, size)

    def on_move(self, event, touch):
        if len(self.touches) > 1:
            return

        x, y = touch.position

        # Compute X/Y relative to the button
        x -= self.x
        y -= self.y

        if self.w > self.h: # Horizontal Slider            
            if x >= 0 and x <= self.w:
                self.value = float(x)/float(self.w)

        elif self.h > self.w: # Vertical Slider
            if y >= 0 and y <= self.h:
                self.value = float(y)/float(self.h)
 

    def render(self, screen):
        thickness = 2
        pygame.draw.rect(screen, self.color, (self.position, self.size), thickness)

        if self.w > self.h:
            pygame.draw.rect(
                    screen, 
                    self.color, 
                    ((self.x + int(self.w*self.value), self.y), 
                    (0, self.h)), 
                    thickness)
        
        elif self.h > self.w:
            pygame.draw.rect(
                    screen, 
                    self.color, 
                    ((self.x, self.y + int(self.h*self.value)), 
                    (self.w, 0)), 
                    thickness)

        text = self.font.render(str(int(self.value * 100)) + '%', 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.x + (self.w/2)
        textpos.centery = self.y + (self.h/2)
        screen.blit(text, textpos)
       

class Button(Widget):

    def __init__(self, label, color, position, size, action):
        super(Button, self).__init__(position, size)

        self.label = label

        self._on_press = action
        self.color =  color
        self.thickness = 2

    def on_press(self, event, touch):
        if callable(self._on_press):
            self._on_press(self, event, touch)

    def render(self, screen):
        thickness = 2
        if self.pressed:
            thickness = 1
        pygame.draw.rect(screen, self.color, (self.position, self.size), thickness)
        text = self.font.render(self.label, 1, self.color)
        textpos = text.get_rect()
        textpos.centerx = self.x + (self.w/2)
        textpos.centery = self.y + (self.h/2)
        screen.blit(text, textpos)

    @property
    def pressed(self):
        return len(self.touches) > 0

pygame.init()

size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

def on_press(event, touch):
    for widget in widgets:
        widget.event(event, touch)

def on_release(event, touch):
    for widget in widgets:
        widget.event(event, touch)

def on_move(event, touch):
    for widget in widgets:
        widget.event(event, touch)

ts = Touchscreen()

for touch in ts.touches:
    touch.on_press = on_press
    touch.on_release = on_release
    touch.on_move = on_move

def button_event(b, e, t):
    print(b.label)

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

ship = [
    Ship((255, 0, 255),(400, 240),(0, 0)),
    Ship((255, 255, 0),(400, 250),(0, 0))]

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ts.stop()
                sys.exit()

    for s in ship:
        s.update()

    screen.fill((0, 0, 0))

    for widget in widgets:
        widget.render(screen)

    pygame.display.flip()

    time.sleep(0.01)
