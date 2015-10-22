#!/usr/bin/env python

import pygame
import signal
import time
import glob
import os
import re
import sys
from pygame.locals import *
from ft5406 import Touchscreen, TS_PRESS
from gui import Button, render_widgets, touchscreen_event

BANK = os.path.join(os.path.dirname(__file__), "sounds")

print("""
This example gives you a simple, ready-to-play instrument which uses .wav files.

For it to work, you must place directories of wav files in:

{}

We've supplied a piano and drums for you to get started with!

Press CTRL+C to exit.
""".format(BANK))

FILETYPES = ['*.wav', '*.ogg']
samples = []
files = []
octave = 0
octaves = 0

patches = glob.glob(os.path.join(BANK, '*'))
patch_index = 0

if len(patches) == 0:
    exit("Couldn't find any .wav files in: {}".format(BANK))


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)]


def load_samples(patch):
    global samples, files, octaves, octave
    files = []
    print('Loading Samples from: {}'.format(patch))
    for filetype in FILETYPES:
        files.extend(glob.glob(os.path.join(patch, filetype)))
    files.sort(key=natural_sort_key)
    octaves = len(files) / 12
    samples = [pygame.mixer.Sound(sample) for sample in files]
    octave = octaves / 2

def handle_instrument(channel, pressed):
    global patch_index
    if pressed:
        patch_index += 1
        patch_index %= len(patches)
        print('Selecting Patch: {}'.format(patches[patch_index]))
        load_samples(patches[patch_index])


def handle_octave_up(channel, pressed):
    global octave
    if pressed and octave < octaves:
        octave += 1
        print('Selected Octave: {}'.format(octave))


def handle_octave_down(channel, pressed):
    global octave
    if pressed and octave > 0:
        octave -= 1
        print('Selected Octave: {}'.format(octave))


def button_event(button, event, touch):
    channel = notes.index(button.label) + (12 * octave)
    if '#' in button.label:
        channel += 1
    channel = int(channel)

    if channel < len(samples) and event == TS_PRESS:
        print('Playing Sound: {}'.format(files[channel]))
        samples[channel].play(loops=0)

def on_ts_event(event, touch):
    touchscreen_event(event, touch)


ts = Touchscreen()

notes = 'c#d#ef#g#a#bC#D#EF#G#A#B'

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

pygame.init()
size = width, height = 800, 480
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

left = 0
last = ''

dimensions = (int(800/len(notes.replace('#',''))),240)

for touch in ts.touches:
    touch.on_press = on_ts_event
    touch.on_release = on_ts_event
    touch.on_move = on_ts_event

for x in notes:
    label = x
    if x == '#':
        label = last + x

    top = 240
    offset_left = 0

    if x == '#':
        top = 0
        offset_left = -int(dimensions[0]/2)

    Button(
        label,
        (255, 0, 0),
        (left + offset_left, top),
        dimensions, 
    button_event)
    
    if x != '#':
        left += dimensions[0]
    
    last = x


load_samples(patches[patch_index])

ts.run()

while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.display.flip()
                ts.stop()
                sys.exit()

    screen.fill((0, 0, 0))

    render_widgets(screen)

    pygame.display.flip()

    time.sleep(0.01)
