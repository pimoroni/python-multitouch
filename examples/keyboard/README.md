# Multitouch Keyboard

Uses the ft5406 driver, Python evdev and Tk to produce a multitouch onscreen keyboard.

Very rough and ready! Focus the main window and hit ESC to exit.

Requires:

```
sudo apt-get install python3-pil python3-pil.imagetk
sudo pip3 install evdev
```

You must also copy the supplied evdev rules into `/etc/evdev/rules.d/`,
create the group 'uinput' and add the user 'pi' to it.
