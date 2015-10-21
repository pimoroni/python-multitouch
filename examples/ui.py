import sys
import pygame
import time
import os
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


class Slider(Widget):

    def __init__(self, min_max, color, position, size, on_change):
        self.min_val, self.max_val = (min_max)
        self.color = color

        self._value_changed = on_change
        
        self.value = self.min_val

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

Button(
    "Quack!",
    (255, 0, 0),
    (20, 20),
    (200, 60), 
    button_event)

Button(
    "Duck!",
    (0,255,0), 
    (20, 100),
    (200, 60), 
    button_event)

Button(
    "Moo!",
    (0, 0, 255),
    (20, 180),
    (200, 60),
    button_event)

for x in range(6):
    Slider(
        (0,100),
        (255, 255, 0),
        (400 + (x*70), 20),
        (40, 400),
        None)

Slider(
    (0,100),
    (0, 255, 255),
    (400,440),
    (400,40),
    None)

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                ts.stop()
                sys.exit()

    screen.fill((0, 0, 0))

    for widget in widgets:
        widget.render(screen)

    pygame.display.flip()

    time.sleep(0.01)
