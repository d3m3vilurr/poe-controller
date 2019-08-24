import os
import sys
from .buttoncode import ButtonCode

if sys.platform == 'win32':
    from .win32 import Win32Mouse as DefaultMouse
elif os.environ.get('SWAYSOCK'):
    from .sway import SwayMouse as DefaultMouse
elif os.environ.get('WAYLAND_DISPLAY'):
    from .uinput import UinputMouse as DefaultMouse
else:
    from .base import BaseMouse as DefaultMouse
