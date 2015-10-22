from ft5406 import Touchscreen, TS_PRESS, TS_RELEASE, TS_MOVE

ts = Touchscreen()

def touch_handler(event, touch):
    if event == TS_PRESS:
        print("Got Press", touch)
    if event == TS_RELEASE:
        print("Got release", touch)
    if event == TS_MOVE:
        print("Got move", touch)

for touch in ts.touches:
    touch.on_press = touch_handler
    touch.on_release = touch_handler
    touch.on_move = touch_handler

ts.run()

while True:
    # Redraw Code etc
    try:
        pass
    except KeyboardInterrupt:
        ts.stop()
        exit()

