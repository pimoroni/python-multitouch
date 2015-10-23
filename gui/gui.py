import sys
import pygame
import time
import os
import math
from numpy import interp
from pygame.locals import *
from ft5406 import TS_PRESS, TS_RELEASE, TS_MOVE

widgets = []


def touchscreen_event(event, touch):
    """Update all widgets with a specific touch event"""
    for widget in widgets:
        widget.event(event, touch)


def render_widgets(screen):
    """Redraw all widgets to screen"""
    for widget in widgets:
        widget.render(screen)


def fullscreen_message(screen, message, color):
    screen.fill((0, 0, 0))
    text(screen, message, (400, 240), 30, color)


def text(screen, text, position, size, color):
    font = pygame.font.Font(None, size)
    text = font.render(text, 1, color)
    textpos = text.get_rect()
    textpos.centerx, textpos.centery = position
    screen.blit(text, textpos)


class Widget:
    
    def __init__(self, position=None, size=None):
        global widgets

        if position is None:
            raise ValueError("Missing required argument position")

        if size is None:
            raise ValueError("Missing required argument size")

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
                self.touches.append(touch)
                if self.active and callable(self.on_press):
                      self.on_press(event, touch)

        """Handle released touches.

        A touch can be released even when its not over a widget.
        """
        if event == TS_RELEASE and touch in self.touches:
            self.touches.remove(touch)
            if self.active and callable(self.on_release):
                self.on_release(event, touch)

        """Handle moving touches.

        Touch movement is tracked even when it's not over a widget
        """
        if event == TS_MOVE and touch in self.touches:
            if self.active and callable(self.on_move):
                self.on_move(event, touch)

    @property
    def position(self):
        return (self.x, self.y)

    @property
    def size(self):
        return (self.w, self.h)


class Dial(Widget):
    
    def __init__(self, min_max=None, color=None, position=None, radius=None, on_change=None):

        if min_max is None:
            raise ValueError("Missing required argument: min_max")
        
        if color is None:
            color = (255, 0, 0)

        if radius is None:
            raise ValueError("Missing required argument: radius")

        self.min_val, self.max_val = (min_max)
        self.color = color
        self.radius = radius
        self.distance = 0

        self._value_changed = on_change

        self.value = 0

        super(Dial, self).__init__(position, (radius*2, radius*2))

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

    def __init__(self, min_max=None, color=None, position=None, size=None, on_change=None):

        if min_max is None:
            raise ValueError("Missing required argument: min_max")

        if color is None:
            color = (255, 0, 0)

        self.min_val, self.max_val, self.default_val = (min_max)
        self.color = color

        self._value_changed = on_change
        
        self.value = interp(self.default_val, [self.min_val, self.max_val], [0, 1])

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

        if callable(self._value_changed):
            new_value = interp(self.value,[0,1],[self.min_val,self.max_val]) 
            self._value_changed(self, new_value)


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

    def __init__(self, label=None, color=None, position=None, size=None, action=None):
        super(Button, self).__init__(position, size)

        if label is None:
            label = ""

        if color is None:
            color = (255, 0, 0)

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

