import win32api
import win32con
import time
import threading
from keyboard.keycode import KeyCode
from keyboard.base import BaseKeyboard

_sended = dict()
_timeout = 0.5

def send_key(vk):
    now = time.time()
    if now - _sended.get(vk, 0) < _timeout:
        return
    win32api.keybd_event(vk, 0, 0, 0)
    _sended[vk] = now
    time.sleep(0.01)
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)


class Win32Keyboard(BaseKeyboard):
    def _key2code(self, key):
        if key == KeyCode.KEY_1:
            return ord('1')
        if key == KeyCode.KEY_2:
            return ord('2')
        if key == KeyCode.KEY_3:
            return ord('3')
        if key == KeyCode.KEY_4:
            return ord('4')
        if key == KeyCode.KEY_5:
            return ord('5')
        if key == KeyCode.KEY_6:
            return ord('6')
        if key == KeyCode.KEY_7:
            return ord('7')
        if key == KeyCode.KEY_Q:
            return ord('Q')
        if key == KeyCode.KEY_W:
            return ord('W')
        if key == KeyCode.KEY_E:
            return ord('E')
        if key == KeyCode.KEY_R:
            return ord('R')
        if key == KeyCode.KEY_T:
            return ord('T')
        if key == KeyCode.KEY_X:
            return ord('X')
        if key == KeyCode.KEY_I:
            return ord('I')
        if key == KeyCode.KEY_ALT:
            return win32con.VK_MENU
        if key == KeyCode.KEY_CTRL:
            return win32con.VK_CONTROL
        if key == KeyCode.KEY_ESC:
            return win32con.VK_ESCAPE
        if key == KeyCode.KEY_TAB:
            return win32con.VK_TAB

    def clicks(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            thread = threading.Thread(target=send_key, args=(code,))
            thread.start()

    def presses(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            win32api.keybd_event(code, 0, 0, 0)

    def releases(self, keys):
        if not len(keys):
            return
        for key in keys:
            code = self._key2code(key)
            if not code:
                continue
            win32api.keybd_event(code, 0, win32con.KEYEVENTF_KEYUP, 0)
