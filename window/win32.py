import win32gui
from window.base import BaseWindow

class Win32Window(BaseWindow):
    def get_window_size(self):
        return (1920, 1080)

    def get_window_offset(self):
        return (0, 0)

    def is_active(self):
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window) == 'Path of Exile'

