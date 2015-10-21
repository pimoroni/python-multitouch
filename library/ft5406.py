import glob
import io
import os
import errno
import struct
from collections import namedtuple

TOUCH_X = 0
TOUCH_Y = 1

TouchEvent = namedtuple('TouchEvent', ('timestamp', 'type', 'code', 'value'))

EV_SYN = 0
EV_ABS = 3

ABS_X = 0
ABS_Y = 1

ABS_MT_SLOT = 0x2f # 47 MT slot being modified
ABS_MT_POSITION_X = 0x35 # 53 Center X of multi touch position
ABS_MT_POSITION_Y = 0x36 # 54 Center Y of multi touch position
ABS_MT_TRACKING_ID = 0x39 # 57 Unique ID of initiated contact

class Touch(object):
    def __init__(self, slot, x, y):
        self.slot = slot
        self.x = x
        self.y = y
        self.id = -1
        self.state = 0  
        
    @property
    def valid(self):
        return self.id > -1

class Touches(list):
    @property
    def valid(self):
        return [touch for touch in self if touch.valid]

class Touchscreen(object):

    TOUCHSCREEN_EVDEV_NAME = 'FT5406 memory based driver'
    EVENT_FORMAT = str('llHHi')
    EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

    def __init__(self):
        self._f_device = io.open(self._touch_device(), 'rb')
        self.position = Touch(0, 0, 0)
        self.touches = Touches([Touch(x, 0, 0) for x in range(10)])
        
        self._touch_slot = 0

    def close(self):
        self._f_device.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def __iter__(self):
        while True:
            event = self._f_device.read(self.EVENT_SIZE)
            (tv_sec, tv_usec, type, code, value) = struct.unpack(self.EVENT_FORMAT, event)
            yield TouchEvent(tv_sec + (tv_usec / 1000000), type, code, value)

    def poll(self):
        while True:
            event = self.read()

            if event.type == EV_SYN: # Sync
                return self.touches
                
            if event.type == EV_ABS: # Absolute cursor position
                if event.code == ABS_MT_SLOT:
                    self._touch_slot = event.value
                    
                if event.code == ABS_MT_TRACKING_ID:
                    self.touches[self._touch_slot].id = event.value
                    
                if event.code == ABS_MT_POSITION_X:
                    self.touches[self._touch_slot].x = event.value
                    
                if event.code == ABS_MT_POSITION_Y:
                    self.touches[self._touch_slot].y = event.value
                    
                if event.code == ABS_X:
                    self.position.x = event.value
                    
                if event.code == ABS_Y:
                    self.position.y = event.value

    def _touch_device(self):
        for evdev in glob.glob("/sys/class/input/event*"):
            try:
                with io.open(os.path.join(evdev, 'device', 'name'), 'r') as f:
                    if f.read().strip() == self.TOUCHSCREEN_EVDEV_NAME:
                        return os.path.join('/dev','input',os.path.basename(evdev))
            except IOError as e:
                if e.errno != errno.ENOENT:
                    raise
            raise RuntimeError('Unable to locate touchscreen device')
        print(devices)

    def read(self):
        return next(iter(self))

    def wait(self, timeout=None):
        pass

if __name__ == "__main__":
    ts = Touchscreen()

    for touches in ts.poll():
        for touch in touches:
            print(touch.slot,touch.valid,touch.x,touch.y)
