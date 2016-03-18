#!/bin/bash

sudo groupadd uinput
sudo usermod -a -G uinput pi
sudo cp 98-keyboard.rules /etc/udev/rules.d/ 
sudo udevadm control --reload
sudo udevadm trigger
sudo modprobe uinput
echo "You should see these permissions: crw-rw---- 1 root uinput ... "
ls -l /dev/uinput
sudo cp multikey /usr/sbin
sudo mkdir -p /usr/share/multikey
sudo sudo cp keyboard.gif /usr/share/multikey/
