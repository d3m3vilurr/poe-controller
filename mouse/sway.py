import enum
import i3ipc
import uinput
from mouse.uinput import UinputMouse


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
        dev = self.point_devices.get(curr.name)
        if dev:
            return dev

        self.point_devices[curr.name] = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            #uinput.REL_X,
            #uinput.REL_Y,
            uinput.ABS_X + (0, curr.rect.width, 0, 0),
            uinput.ABS_Y + (0, curr.rect.height, 0, 0),
        ])
        return self.point_devices[curr.name]
