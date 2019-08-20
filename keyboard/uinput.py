import uinput
from keyboard.keycode import KeyCode
from keyboard.base import BaseKeyboard

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

    def input(self, keys):
        if not len(keys):
            return
        combos = []
        for key in keys:
            if key == KeyCode.KEY_1:
                self.device.emit_click(uinput.KEY_1, syn=False)
            if key == KeyCode.KEY_2:
                self.device.emit_click(uinput.KEY_2, syn=False)
            if key == KeyCode.KEY_3:
                self.device.emit_click(uinput.KEY_3, syn=False)
            if key == KeyCode.KEY_4:
                self.device.emit_click(uinput.KEY_4, syn=False)
            if key == KeyCode.KEY_5:
                self.device.emit_click(uinput.KEY_5, syn=False)
            if key == KeyCode.KEY_6:
                self.device.emit_click(uinput.KEY_6, syn=False)
            if key == KeyCode.KEY_7:
                self.device.emit_click(uinput.KEY_7, syn=False)
            if key == KeyCode.KEY_Q:
                self.device.emit_click(uinput.KEY_Q, syn=False)
            if key == KeyCode.KEY_W:
                self.device.emit_click(uinput.KEY_W, syn=False)
            if key == KeyCode.KEY_E:
                self.device.emit_click(uinput.KEY_E, syn=False)
            if key == KeyCode.KEY_R:
                self.device.emit_click(uinput.KEY_R, syn=False)
            if key == KeyCode.KEY_T:
                self.device.emit_click(uinput.KEY_T, syn=False)
            if key == KeyCode.KEY_X:
                self.device.emit_click(uinput.KEY_X, syn=False)
            if key == KeyCode.KEY_I:
                self.device.emit_click(uinput.KEY_I, syn=False)
            if key == KeyCode.KEY_ALT:
                self.device.emit_click(uinput.KEY_LEFTALT, syn=False)
            if key == KeyCode.KEY_CTRL:
                self.device.emit_click(uinput.KEY_LEFTCTRL, syn=False)
            if key == KeyCode.KEY_ESC:
                self.device.emit_click(uinput.KEY_ESC, syn=False)
            if key == KeyCode.KEY_TAB:
                self.device.emit_click(uinput.KEY_TAB, syn=False)
        self.device.syn()

    def press(self, key, release=False):
        if key == KeyCode.KEY_ALT:
            inp = uinput.KEY_LEFTALT
        else:
            return
        self.device.emit(inp, 0 if release else 1)
