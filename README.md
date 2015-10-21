# Python FT5406 Multitouch Driver

Multi-touch pure Python driver for the official 7" touchscreen display.

# Beta

This is a work in progress, but lets you use all 10 points of multitouch on the official 7" Pi Touchscreen in Python.

# Installing

Navigate into the library folder, and run setup like so:

```bash
cd library
sudo python3 setup.py install
```

See the examples folder for usage!

# Using The Library

```python
import ft5406
ts = ft5406.Touchscreen()

while True:
    for touch in ts.poll():
        print(touch.slot, touch.id, touch.valid, touch.x, touch.y)
```

The `slot` is a number from 0 to 9, denoting which index the touch is at.

The touch `id` is a unique ID given to the touch by evdev.

Touch `valid` indicates whether the touch is active- ie: is synonymous to `pressed`.

Both `x` and `y` should be self explanatory!

# TODO

I love event-driven code, so I'd like to rebuild this to work on an event driven basis- calling bound functions
when a touch is acquired, lost or moved. Something like ( This is hypothetical, not actual code! ):

```
@ts.on_move
def on_move(touch):
    print("Touch {} moved to {}{}".format(touch.index, touch.x, touch.y))

@ts.on_touch
def on_touch(touch):
    print("Touch started at {} {}".format(touch.x, touch.y))
    
@ts.on_release
def on_release(touch):
    print("Touch ended at {} {}".format(touch.x, touch.y))
```
