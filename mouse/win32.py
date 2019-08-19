import win32api

class Win32Mouse(object):
    def move(self, x, y, relative=False):
        if not relative:
            win32api.SetCursorPos((x, y))
        else:
            _x, _y = win32api.GetCursorPos()
            win32api.SetCursorPos((_x + x, _y + y))

    def left(self, on=True):
        pass

    def middle(self, on=True):
        pass

    def right(self, on=True):
        pass

