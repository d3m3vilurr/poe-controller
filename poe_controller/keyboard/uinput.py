import uinput
from .keycode import KeyCode
from .base import BaseKeyboard

class UinputKeyboard(BaseKeyboard):
    def __init__(self):
        self.device = uinput.Device([
            uinput.KEY_1,
            uinput.KEY_2,
            uinput.KEY_3,
            uinput.KEY_4,
            uinput.KEY_5,
            uinput.KEY_6,
            uinput.KEY_7,
            uinput.KEY_Q,
            uinput.KEY_W,
            uinput.KEY_E,
            uinput.KEY_R,
            uinput.KEY_T,
            uinput.KEY_X,
            uinput.KEY_I,
            uinput.KEY_LEFTALT,
            uinput.KEY_LEFTCTRL,
            uinput.KEY_ESC,
            uinput.KEY_TAB,
        ])

    def _key2code(self, key):
        if key == KeyCode.KEY_1:
            return uinput.KEY_1
        if key == KeyCode.KEY_2:
            return uinput.KEY_2
        if key == KeyCode.KEY_3:
            return uinput.KEY_3
        if key == KeyCode.KEY_4:
            return uinput.KEY_4
        if key == KeyCode.KEY_5:
            return uinput.KEY_5
        if key == KeyCode.KEY_6:
            return uinput.KEY_6
        if key == KeyCode.KEY_7:
            return uinput.KEY_7
        if key == KeyCode.KEY_Q:
            return uinput.KEY_Q
        if key == KeyCode.KEY_W:
            return uinput.KEY_W
        if key == KeyCode.KEY_E:
            return uinput.KEY_E
        if key == KeyCode.KEY_R:
            return uinput.KEY_R
        if key == KeyCode.KEY_T:
            return uinput.KEY_T
        if key == KeyCode.KEY_X:
            return uinput.KEY_X
        if key == KeyCode.KEY_I:
            return uinput.KEY_I
        if key == KeyCode.KEY_ALT:
            return uinput.KEY_LEFTALT
        if key == KeyCode.KEY_CTRL:
            return uinput.KEY_LEFTCTRL
        if key == KeyCode.KEY_ESC:
            return uinput.KEY_ESC
        if key == KeyCode.KEY_TAB:
            return uinput.KEY_TAB

    def clicks(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            self.device.emit_click(code, syn=False)
        self.device.syn()

    def presses(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            self.device.emit(code, 1, syn=False)
        self.device.syn()

    def releases(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            self.device.emit(code, 0, syn=False)
        self.device.syn()
