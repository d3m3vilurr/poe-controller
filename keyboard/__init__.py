import os

from keyboard.keycode import KeyCode

if os.environ.get('WAYLAND_DISPLAY'):
    from keyboard.uinput import UinputKeyboard as DefaultKeyboard
else:
    from keyboard.base import BaseKeyboard as DefaultKeyboard
