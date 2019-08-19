import os
import sys
from keyboard.keycode import KeyCode

if sys.platform == 'win32':
    from keyboard.win32 import Win32Keyboard as DefaultKeyboard
elif os.environ.get('WAYLAND_DISPLAY'):
    from keyboard.uinput import UinputKeyboard as DefaultKeyboard
else:
    from keyboard.base import BaseKeyboard as DefaultKeyboard
