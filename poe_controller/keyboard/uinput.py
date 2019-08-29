import uinput
import enum
import time
from multiprocessing import Process, Manager, Queue
from .keycode import KeyCode
from .base import BaseKeyboard


class UinputKeyboardAction(enum.Enum):
    KEY_CLICK = 1
    KEY_PRESS = 2
    KEY_RELEASE= 3


def input_worker(shared, queue):
    dev = uinput.Device([
        uinput.KEY_1,
        uinput.KEY_2,
        uinput.KEY_3,
        uinput.KEY_4,
        uinput.KEY_5,
        uinput.KEY_6,
        uinput.KEY_7,
        uinput.KEY_E,
        uinput.KEY_I,
        uinput.KEY_Q,
        uinput.KEY_R,
        uinput.KEY_T,
        uinput.KEY_W,
        uinput.KEY_X,
        uinput.KEY_Z,
        uinput.KEY_LEFTALT,
        uinput.KEY_LEFTCTRL,
        uinput.KEY_ESC,
        uinput.KEY_TAB,
    ])
    while (shared.alive):
        if not queue.qsize():
            time.sleep(0.01)
            continue
        inp = queue.get()
        act, keys = inp[:2]
        if act == UinputKeyboardAction.KEY_CLICK:
            for key in keys:
                dev.emit_click(key, syn=False)
            dev.syn()
        elif act == UinputKeyboardAction.KEY_PRESS:
            for key in keys:
                dev.emit(key, 1, syn=False)
            dev.syn()
        elif act == UinputKeyboardAction.KEY_RELEASE:
            for key in keys:
                dev.emit(key, 0, syn=False)
            dev.syn()


class UinputKeyboard(BaseKeyboard):
    def __init__(self):
        process_manager = Manager()
        self._shared_data = process_manager.Namespace()
        self._shared_data.alive = True

        self._queue = Queue()
        self._worker = Process(target=input_worker, args=(self._shared_data, self._queue))
        self._worker.start()

    def __del__(self):
        if self._worker.is_alive():
            self._shared_data.alive = False
            self._worker.join()

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
        if key == KeyCode.KEY_E:
            return uinput.KEY_E
        if key == KeyCode.KEY_I:
            return uinput.KEY_I
        if key == KeyCode.KEY_Q:
            return uinput.KEY_Q
        if key == KeyCode.KEY_R:
            return uinput.KEY_R
        if key == KeyCode.KEY_T:
            return uinput.KEY_T
        if key == KeyCode.KEY_W:
            return uinput.KEY_W
        if key == KeyCode.KEY_X:
            return uinput.KEY_X
        if key == KeyCode.KEY_Z:
            return uinput.KEY_Z
        if key == KeyCode.KEY_ALT:
            return uinput.KEY_LEFTALT
        if key == KeyCode.KEY_CTRL:
            return uinput.KEY_LEFTCTRL
        if key == KeyCode.KEY_SHIFT:
            return uinput.KEY_LEFTSHIFT
        if key == KeyCode.KEY_ESC:
            return uinput.KEY_ESC
        if key == KeyCode.KEY_TAB:
            return uinput.KEY_TAB

    def clicks(self, keys):
        if not len(keys):
            return
        self._queue.put((UinputKeyboardAction.KEY_CLICK,
                         tuple(filter(None, (self._key2code(key) for key in keys)))))

    def presses(self, keys):
        if not len(keys):
            return
        self._queue.put((UinputKeyboardAction.KEY_PRESS,
                         tuple(filter(None, (self._key2code(key) for key in keys)))))

    def releases(self, keys):
        if not len(keys):
            return
        self._queue.put((UinputKeyboardAction.KEY_RELEASE,
                         tuple(filter(None, (self._key2code(key) for key in keys)))))
