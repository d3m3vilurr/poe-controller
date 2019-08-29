import enum
import i3ipc
import uinput
from .uinput import UinputMouse


class SwayMouse(UinputMouse):

    def __init__(self):
        super(SwayMouse, self).__init__()
        self.i3 = i3ipc.Connection()
        self.point_devices = {}
        self._BTN = {}

    def _get_current_input_device(self):
        outputs = self.i3.get_outputs()
        for output in outputs:
            if not output.focused:
                continue
            curr = output
        if not curr:
            return self.default_device

        if hasattr(self._shared_data, curr.name):
            return curr.name

        setattr(self._shared_data, curr.name, [
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            #uinput.REL_X,
            #uinput.REL_Y,
            uinput.ABS_X + (0, curr.rect.width, 0, 0),
            uinput.ABS_Y + (0, curr.rect.height, 0, 0),
        ])

        return curr.name
