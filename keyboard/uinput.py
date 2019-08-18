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
            uinput.KEY_LEFTALT,
            uinput.KEY_LEFTCTRL,
            uinput.KEY_ESC,
        ])

    def input(self, keys):
        if not len(keys):
            return
        combos = []
        for key in keys:
            if key == KeyCode.KEY_1:
                combos.append(uinput.KEY_1)
            if key == KeyCode.KEY_2:
                combos.append(uinput.KEY_2)
            if key == KeyCode.KEY_3:
                combos.append(uinput.KEY_3)
            if key == KeyCode.KEY_4:
                combos.append(uinput.KEY_4)
            if key == KeyCode.KEY_5:
                combos.append(uinput.KEY_5)
            if key == KeyCode.KEY_6:
                combos.append(uinput.KEY_6)
            if key == KeyCode.KEY_7:
                combos.append(uinput.KEY_7)
            if key == KeyCode.KEY_Q:
                combos.append(uinput.KEY_Q)
            if key == KeyCode.KEY_W:
                combos.append(uinput.KEY_W)
            if key == KeyCode.KEY_E:
                combos.append(uinput.KEY_E)
            if key == KeyCode.KEY_R:
                combos.append(uinput.KEY_R)
            if key == KeyCode.KEY_T:
                combos.append(uinput.KEY_T)
            if key == KeyCode.KEY_X:
                combos.append(uinput.KEY_X)
            if key == KeyCode.KEY_ALT:
                combos.append(uinput.KEY_LEFTALT)
            if key == KeyCode.KEY_CTRL:
                combos.append(uinput.KEY_LEFTCTRL)
            if key == KeyCode.KEY_ESC:
                combos.append(uinput.KEY_ESC)
        self.device.emit_combo(combos)

    def press(self, key, release=False):
        if key == KeyCode.KEY_ALT:
            inp = uinput.KEY_LEFTALT
        else:
            return
        self.device.emit(inp, 0 if release else 1)
