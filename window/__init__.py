import os
import sys

if sys.platform == 'win32':
    from window.win32 import Win32Window as DefaultWindow
elif os.environ.get('SWAYSOCK'):
    from window.sway import SwayWindow as DefaultWindow
#elif os.environ.get('WAYLAND_DISPLAY'):
#    pass
else:
    from window.base import BaseWindow as DefaultWindow
