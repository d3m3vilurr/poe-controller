import win32api
import win32con
import time
import threading
from keyboard.keycode import KeyCode
from keyboard.base import BaseKeyboard

_sended = dict()
_timeout = 0.5

def send_key(vks):
    fired = []
    now = time.time()
    for vk in vks:
        if now - _sended.get(vk, 0) < _timeout:
            continue
        win32api.keybd_event(vk, 0, 0, 0)
        fired.append(vk)
        _sended[vk] = now

    time.sleep(0.01)
    for vk in fired:
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)


class Win32Keyboard(BaseKeyboard):
    def input(self, keys):
        if not len(keys):
            return
        combos = []
        for key in keys:
            if key == KeyCode.KEY_1:
                combos.append(ord('1'))
            if key == KeyCode.KEY_2:
                combos.append(ord('2'))
            if key == KeyCode.KEY_3:
                combos.append(ord('3'))
            if key == KeyCode.KEY_4:
                combos.append(ord('4'))
            if key == KeyCode.KEY_5:
                combos.append(ord('5'))
            if key == KeyCode.KEY_6:
                combos.append(ord('6'))
            if key == KeyCode.KEY_7:
                combos.append(ord('7'))
            if key == KeyCode.KEY_Q:
                combos.append(ord('Q'))
            if key == KeyCode.KEY_W:
                combos.append(ord('W'))
            if key == KeyCode.KEY_E:
                combos.append(ord('E'))
            if key == KeyCode.KEY_R:
                combos.append(ord('R'))
            if key == KeyCode.KEY_T:
                combos.append(ord('T'))
            if key == KeyCode.KEY_X:
                combos.append(ord('X'))
            if key == KeyCode.KEY_I:
                combos.append(ord('I'))
            if key == KeyCode.KEY_ALT:
                combos.append(win32con.VK_MENU)
            if key == KeyCode.KEY_CTRL:
                combos.append(win32con.VK_CONTROL)
            if key == KeyCode.KEY_ESC:
                combos.append(win32con.VK_ESCAPE)
            if key == KeyCode.KEY_TAB:
                combos.append(win32con.VK_TAB)
        thread = threading.Thread(target=send_key, args=(combos,))
        thread.start()


    def press(self, key, release=False):
        if key == KeyCode.KEY_ALT:
            inp = win32con.VK_MENU
        else:
            return
        win32api.keybd_event(inp, 0, win32con.KEYEVENTF_KEYUP if release else 0, 0)
