import win32api
import win32con
import enum
from mouse.base import BaseMouse


class Win32MouseButton(enum.Enum):
    LEFT=1
    RIGHT=2
    MIDDLE=3


class Win32Mouse(BaseMouse):
    def __init__(self):
        self._BTN = {}

    def move(self, x, y, relative=False):
        if not relative:
            win32api.SetCursorPos((x, y))
        else:
            _x, _y = win32api.GetCursorPos()
            win32api.SetCursorPos((_x + x, _y + y))

    def left(self, on=True):
        print(on)
        if on:
            self._press(Win32MouseButton.LEFT)
        else:
            self._release(Win32MouseButton.LEFT)

    def middle(self, on=True):
        if on:
            self._press(Win32MouseButton.MIDDLE)
        else:
            self._release(Win32MouseButton.MIDDLE)

    def right(self, on=True):
        if on:
            self._press(Win32MouseButton.RIGHT)
        else:
            self._release(Win32MouseButton.RIGHT)

    def _press(self, btn):
        if self._BTN.get(btn, False):
            return
        if btn == Win32MouseButton.LEFT:
            event = win32con.MOUSEEVENTF_LEFTDOWN
        elif btn == Win32MouseButton.RIGHT:
            event = win32con.MOUSEEVENTF_RIGHTDOWN
        elif btn == Win32MouseButton.MIDDLE:
            event = win32con.MOUSEEVENTF_MIDDLEDOWN
        win32api.mouse_event(event, 0, 0, 0, 0)
        self._BTN[btn] = True

    def _release(self, btn):
        if not self._BTN.get(btn, False):
            return
        if btn == Win32MouseButton.LEFT:
            event = win32con.MOUSEEVENTF_LEFTUP
        elif btn == Win32MouseButton.RIGHT:
            event = win32con.MOUSEEVENTF_RIGHTUP
        elif btn == Win32MouseButton.MIDDLE:
            event = win32con.MOUSEEVENTF_MIDDLEUP
        win32api.mouse_event(event, 0, 0, 0, 0)
        self._BTN[btn] = False


