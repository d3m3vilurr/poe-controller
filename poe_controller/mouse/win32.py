import win32api
import win32con
import enum
from .base import BaseMouse
from .buttoncode import ButtonCode


class Win32Mouse(BaseMouse):
    def move(self, x, y, relative=False):
        if not relative:
            win32api.SetCursorPos((x, y))
        else:
            _x, _y = win32api.GetCursorPos()
            win32api.SetCursorPos((_x + x, _y + y))

    def _btn2eventcode(self, btn, on):
        if on:
            if btn == ButtonCode.LEFT:
                return win32con.MOUSEEVENTF_LEFTDOWN
            if btn == ButtonCode.RIGHT:
                return win32con.MOUSEEVENTF_RIGHTDOWN
            if btn == ButtonCode.MIDDLE:
                return win32con.MOUSEEVENTF_MIDDLEDOWN
        else:
            if btn == ButtonCode.LEFT:
                return win32con.MOUSEEVENTF_LEFTUP
            if btn == ButtonCode.RIGHT:
                return win32con.MOUSEEVENTF_RIGHTUP
            if btn == ButtonCode.MIDDLE:
                return win32con.MOUSEEVENTF_MIDDLEUP

    def presses(self, buttons):
        if not len(buttons):
            return
        for btn in buttons:
            code = self._btn2eventcode(btn, True)
            if not code:
                continue
            win32api.mouse_event(code, 0, 0, 0, 0)

    def releases(self, buttons):
        if not len(buttons):
            return
        for btn in buttons:
            code = self._btn2eventcode(btn, False)
            if not code:
                continue
            win32api.mouse_event(code, 0, 0, 0, 0)
