import win32gui
from .base import BaseWindow

class Win32Window(BaseWindow):
    def __init__(self):
        self._curr_win_rect = (0, 0, 0, 0)

    def get_window_size(self):
        if not self.is_active():
            return (0, 0)
        return self._curr_win_rect[-2:]

    def get_window_offset(self):
        if not self.is_active():
            return (0, 0)
        offset = self._curr_win_rect[:2]
        _, height = self.get_window_size()
        return (offset[0], offset[1] - int(height / 20))

    def get_radius(self):
        if not self.is_active():
            return 0
        _, height = self.get_window_size()
        return int(height / 5)

    def is_active(self):
        try:
            self._curr_win = win32gui.GetForegroundWindow()
            l, t, r, b = win32gui.GetWindowRect(self._curr_win)
            self._curr_win_rect = (l, t, r - l, b - t)
            return win32gui.GetWindowText(self._curr_win) == 'Path of Exile'
        except:
            return False
