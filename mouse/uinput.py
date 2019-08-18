import uinput
from mouse.base import BaseMouse

class UinputMouse(BaseMouse):

    def __init__(self):
        self.device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            uinput.REL_X,
            uinput.REL_Y,
        ])
        self._BTN = {}

    def move(self, x, y, relative=False):
        if not relative:
            # move 0, 0
            self.device.emit(uinput.REL_X, -65536)
            self.device.emit(uinput.REL_Y, -65536)
        self.device.emit(uinput.REL_X, int(x))
        self.device.emit(uinput.REL_Y, int(y))

    def left(self, on=True):
        self._click(uinput.BTN_LEFT, on)

    def middle(self, on=True):
        self._click(uinput.BTN_MIDDLE, on)

    def right(self, on=True):
        self._click(uinput.BTN_RIGHT, on)

    def _click(self, btn, on=True):
        if self._BTN.get(btn, False) == on:
            return
        self.device.emit(btn, on and 1 or 0)
        self._BTN[btn] = on

