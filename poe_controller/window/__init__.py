import os
import sys

if sys.platform == 'win32':
    from .win32 import Win32Window as DefaultWindow
elif os.environ.get('SWAYSOCK'):
    from .sway import SwayWindow as DefaultWindow
#elif os.environ.get('WAYLAND_DISPLAY'):
#    pass
else:
    from .base import BaseWindow as DefaultWindow
