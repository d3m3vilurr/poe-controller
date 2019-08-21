import os
import sys
from .keycode import KeyCode

if sys.platform == 'win32':
    from .win32 import Win32Keyboard as DefaultKeyboard
elif os.environ.get('WAYLAND_DISPLAY'):
    from .uinput import UinputKeyboard as DefaultKeyboard
else:
    from .base import BaseKeyboard as DefaultKeyboard
