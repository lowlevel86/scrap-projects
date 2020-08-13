#!/bin/bash

# set XKB layout
setxkbmap -layout us

# turn on mousekeys
xkbset m

# stop mousekeys expiring after a timeout
xkbset exp =m

# Note: run xev to find keycodes
xmodmap -e "keycode 133 = Pointer_Button2"
