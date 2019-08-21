import os
import sys

if sys.platform == 'win32':
    from mouse.win32 import Win32Mouse as DefaultMouse
elif os.environ.get('SWAYSOCK'):
    from mouse.sway import SwayMouse as DefaultMouse
elif os.environ.get('WAYLAND_DISPLAY'):
    from mouse.uinput import UinputMouse as DefaultMouse
else:
    from mouse.base import BaseMouse as DefaultMouse
