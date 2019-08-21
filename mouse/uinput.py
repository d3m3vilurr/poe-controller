import uinput
from mouse.base import BaseMouse
import time

TIMEOUT = 0.03

class UinputMouse(BaseMouse):

    def __init__(self):
        self.default_device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            uinput.REL_X,
            uinput.REL_Y,
            # TODO detect full screen size
            uinput.ABS_X + (0, 1920, 0, 0),
            uinput.ABS_Y + (0, 1080, 0, 0),
        ])
        #self._last_move_time = 0
        self._BTN = {}

    def _get_current_input_device(self):
        return self.default_device

    def move(self, x, y, relative=False):
        now = time.time()
        if not relative:
            # XXX: this timecheck would reduce the input delay
            #if now - self._last_move_time < TIMEOUT:
            #    return
            device = self._get_current_input_device()
            device.emit(uinput.ABS_X, int(x), syn=False)
            device.emit(uinput.ABS_Y, int(y), syn=False)
            device.syn()
            #self._last_move_time = now
        else:
            self.default_device.emit(uinput.REL_X, int(x), syn=False)
            self.default_device.emit(uinput.REL_Y, int(y), syn=False)
            self.default_device.syn()

    def left(self, on=True):
        self._click(uinput.BTN_LEFT, on)

    def middle(self, on=True):
        self._click(uinput.BTN_MIDDLE, on)

    def right(self, on=True):
        self._click(uinput.BTN_RIGHT, on)

    def _click(self, btn, on=True):
        if self._BTN.get(btn, False) == on:
            return
        self.default_device.emit(btn, on and 1 or 0)
        self._BTN[btn] = on
