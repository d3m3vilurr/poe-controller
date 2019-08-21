import i3ipc
from .base import BaseWindow

class SwayWindow(BaseWindow):
    def __init__(self):
        self.i3 = i3ipc.Connection()
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
            self._curr_win = self.i3.get_tree().find_focused()
            rect = self._curr_win.rect
            self._curr_win_rect = (rect.x, rect.y, rect.width, rect.height)
            return self._curr_win.name == 'Path of Exile'
        except:
            return False
