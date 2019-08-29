import i3ipc
import time
from .base import BaseWindow
from multiprocessing import Process, Manager, Lock


def info_worker(lock, shared):
    i3 = i3ipc.Connection()

    while shared.alive:
        curr_win = i3.get_tree().find_focused()

        if curr_win.name == 'Path of Exile':
            if shared.actived:
                time.sleep(0.01)
                continue
            lock.acquire()
            rect = curr_win.rect
            shared.win_rect = (rect.x, rect.y, rect.width, rect.height)
            shared.actived = True
            lock.release()
        else:
            if not shared.actived:
                time.sleep(0.01)
                continue
            lock.acquire()
            shared.win_rect = (0, 0, 0, 0)
            shared.actived = False
            lock.release()



class SwayWindow(BaseWindow):
    def __init__(self):
        self.i3 = i3ipc.Connection()
        self._actived = False
        self._win_rect = (0, 0, 0, 0)

        process_manager = Manager()
        self._shared_data = process_manager.Namespace()
        self._shared_data.alive = True
        self._shared_data.actived = False
        self._lock = Lock()
        self._worker = Process(target=info_worker, args=(self._lock, self._shared_data))
        self._worker.start()

    def __del__(self):
        if self._worker.is_alive():
            self._shared_data.alive = False
            self._worker.join()

    def get_window_size(self):
        return self._win_rect[-2:]

    def get_window_offset(self):
        offset = self._win_rect[:2]
        _, height = self.get_window_size()
        return (offset[0], offset[1] - int(height / 20))

    def get_radius(self):
        if not self._actived:
            return 0
        _, height = self.get_window_size()
        return int(height / 5)

    def is_active(self):
        if self._actived != self._shared_data.actived:
            self._lock.acquire()
            self._actived = self._shared_data.actived
            self._win_rect = self._shared_data.win_rect
            self._lock.release()
        return self._actived
