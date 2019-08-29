import uinput
from multiprocessing import Process, Manager, Queue
from .base import BaseMouse
from .buttoncode import ButtonCode
import time
import enum


class UinputMouseAction(enum.Enum):
    ABS_MOVE = 1
    REL_MOVE = 2
    KEY_PRESS = 3
    KEY_RELEASE= 4


def input_worker(shared, queue):
    devices = dict()
    while (shared.alive):
        if not queue.qsize():
            time.sleep(0.01)
            continue
        inp = queue.get()
        dev_key, act = inp[:2]
        dev = devices.get(dev_key)
        if not dev:
            dev_option = getattr(shared, dev_key)
            dev = devices[dev_key] = uinput.Device(dev_option)
        if act == UinputMouseAction.ABS_MOVE:
            pos = inp[2]
            dev.emit(uinput.ABS_X, pos[0], syn=False)
            dev.emit(uinput.ABS_Y, pos[1], syn=False)
            dev.syn()
        elif act == UinputMouseAction.REL_MOVE:
            pos = inp[2]
            dev.emit(uinput.REL_X, pos[0], syn=False)
            dev.emit(uinput.REL_Y, pos[1], syn=False)
            dev.syn()
        elif act == UinputMouseAction.KEY_PRESS:
            btns = inp[2]
            for btn in btns:
                dev.emit(btn, 1, syn=False)
            dev.syn()
        elif act == UinputMouseAction.KEY_RELEASE:
            btns = inp[2]
            for btn in btns:
                dev.emit(btn, 0, syn=False)
            dev.syn()


class UinputMouse(BaseMouse):
    def __init__(self):
        process_manager = Manager()
        self._shared_data = process_manager.Namespace()
        self._shared_data.alive = True
        self._shared_data.DEFAULT_MOUSE = [
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            uinput.REL_X,
            uinput.REL_Y,
            # TODO detect full screen size
            uinput.ABS_X + (0, 1920, 0, 0),
            uinput.ABS_Y + (0, 1080, 0, 0),
        ]

        self._queue = Queue()
        self._worker = Process(target=input_worker, args=(self._shared_data, self._queue))
        self._worker.start()

    def __del__(self):
        if self._worker.is_alive():
            self._shared_data.alive = False
            self._worker.join()

    def _get_current_input_device_key(self):
        return 'DEFAULT_MOUSE'

    def move(self, x, y, relative=False):
        now = time.time()
        if not relative:
            device = self._get_current_input_device_key()
            self._queue.put((device,
                             UinputMouseAction.ABS_MOVE,
                             (int(x), int(y))))
        else:
            self._queue.put(('DEFAULT_MOUSE',
                             UinputMouseAction.REL_MOVE,
                             (int(x), int(y))))

    def _btn2code(self, btn):
        if btn == ButtonCode.LEFT:
            return uinput.BTN_LEFT
        if btn == ButtonCode.RIGHT:
            return uinput.BTN_RIGHT
        if btn == ButtonCode.MIDDLE:
            return uinput.BTN_MIDDLE

    def presses(self, buttons):
        if not len(buttons):
            return
        device = self._get_current_input_device()
        self._queue.put((device,
                         UinputMouseAction.KEY_PRESS,
                         tuple(filter(None, (self._btn2code(btn) for btn in buttons)))))

    def releases(self, buttons):
        if not len(buttons):
            return
        device = self._get_current_input_device()
        self._queue.put((device,
                         UinputMouseAction.KEY_RELEASE,
                         tuple(filter(None, (self._btn2code(btn) for btn in buttons)))))
