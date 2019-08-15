"""Simple gamepad/joystick test example."""

from __future__ import print_function
import inputs
import uinput
import math
import enum

# TODO get right size from application
SCREEN_X = 1920
SCREEN_Y = 1080
# don't know reason wayland use half
SCREEN_X = 1920 / 2
SCREEN_Y = 1080 / 2
DISTANCE = 50

MOVE_THRESHOLD = 20

KEY_INPUT_DELAY = 10

def angle(x, y):
    return math.atan2(y, x)

def move_distance(angle, distance=DISTANCE):
    return int(distance * math.cos(angle)), int(distance * math.sin(angle))

class Mouse(object):
    def move(self, x, y, relative=False):
        pass

    def left(self):
        pass

    def middle(self):
        pass

    def right(self):
        pass

class KeyCode(enum.Enum):
    KEY_1 = 1
    KEY_2 = 2
    KEY_3 = 3
    KEY_4 = 4
    KEY_5 = 5
    KEY_6 = 6
    KEY_7 = 7
    KEY_Q = 10
    KEY_W = 11
    KEY_E = 12
    KEY_R = 13
    KEY_T = 14
    KEY_X = 15
    KEY_ALT = 30
    KEY_CTRL = 31
    KEY_ESC = 32

class Keyboard(object):
    def input(self, keys):
        pass

    def press(self, key, release=False):
        pass

class UinputMouse(Mouse):

    def __init__(self):
        self.device = uinput.Device([
            uinput.BTN_LEFT,
            uinput.BTN_RIGHT,
            uinput.BTN_MIDDLE,
            uinput.REL_X,
            uinput.REL_Y,
        ])
        self._BTN = {}

    def move(self, x, y, relative=False):
        if not relative:
            # move 0, 0
            self.device.emit(uinput.REL_X, -65536)
            self.device.emit(uinput.REL_Y, -65536)
        self.device.emit(uinput.REL_X, int(x))
        self.device.emit(uinput.REL_Y, int(y))

    def left(self, on=True):
        self._click(uinput.BTN_LEFT, on)

    def middle(self, on=True):
        self._click(uinput.BTN_MIDDLE, on)

    def right(self, on=True):
        self._click(uinput.BTN_RIGHT, on)

    def _click(self, btn, on=True):
        if self._BTN.get(btn, False) == on:
            return
        self.device.emit(btn, on and 1 or 0)
        self._BTN[btn] = on

class UinputKeyboard(Keyboard):
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

EVENT_ABB = (
    # D-PAD, aka HAT
    ('Absolute-ABS_HAT0X', 'HX'),
    ('Absolute-ABS_HAT0Y', 'HY'),

    # Analogs
    ('Absolute-ABS_X', 'LX'),
    ('Absolute-ABS_Y', 'LY'),
    ('Absolute-ABS_RX', 'RX'),
    ('Absolute-ABS_RY', 'RY'),
    ('Absolute-ABS_LZ', 'LZ'),
    ('Absolute-ABS_RZ', 'RZ'),

    # Face Buttons
    ('Key-BTN_NORTH', 'N'),
    ('Key-BTN_EAST', 'E'),
    ('Key-BTN_SOUTH', 'S'),
    ('Key-BTN_WEST', 'W'),

    # Other buttons
    ('Key-BTN_THUMBL', 'THL'),
    ('Key-BTN_THUMBR', 'THR'),
    ('Key-BTN_TL', 'TL'),
    ('Key-BTN_TR', 'TR'),
    ('Key-BTN_TL2', 'TL2'),
    ('Key-BTN_TR2', 'TR3'),
    ('Key-BTN_MODE', 'M'),
    ('Key-BTN_START', 'ST'),

    # PiHUT SNES style controller buttons
    ('Key-BTN_TRIGGER', 'N'),
    ('Key-BTN_THUMB', 'E'),
    ('Key-BTN_THUMB2', 'S'),
    ('Key-BTN_TOP', 'W'),
    ('Key-BTN_BASE3', 'SL'),
    ('Key-BTN_BASE4', 'ST'),
    ('Key-BTN_TOP2', 'TL'),
    ('Key-BTN_PINKIE', 'TR')
)


# This is to reduce noise from the PlayStation controllers
# For the Xbox controller, you can set this to 0
MIN_ABS_DIFFERENCE = 5


class Controller(object):
    """Simple joystick test class."""
    def __init__(self, gamepad=None, keyboard=None, mouse=None, abbrevs=EVENT_ABB):
        self.btn_state = {}
        self.old_btn_state = {}
        self.abs_state = {}
        self.old_abs_state = {}
        self.abbrevs = dict(abbrevs)
        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.abs_state[value] = 128
                self.old_abs_state[value] = 128
            if key.startswith('Key'):
                self.btn_state[value] = 0
                self.old_btn_state[value] = 0
        self._other = 0
        self.gamepad = gamepad
        if not gamepad:
            self._get_gamepad()
        if not mouse:
            mouse = Mouse()
        if not keyboard:
            keyboard = Keyboard()
        self.mouse = mouse
        self.keyboard = keyboard
        self.mouse_mode = 0

    def _get_gamepad(self):
        """Get a gamepad object."""
        try:
            self.gamepad = inputs.devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError("No gamepad found.")

    def handle_unknown_event(self, event, key):
        """Deal with unknown events."""
        if event.ev_type == 'Key':
            new_abbv = 'B' + str(self._other)
            self.btn_state[new_abbv] = 0
            self.old_btn_state[new_abbv] = 0
        elif event.ev_type == 'Absolute':
            new_abbv = 'A' + str(self._other)
            self.abs_state[new_abbv] = 0
            self.old_abs_state[new_abbv] = 0
        else:
            return None

        self.abbrevs[key] = new_abbv
        self._other += 1

        return self.abbrevs[key]

    def process_event(self, event):
        """Process the event into a state."""
        if event.ev_type == 'Sync':
            return
        if event.ev_type == 'Misc':
            return
        key = event.ev_type + '-' + event.code
        try:
            abbv = self.abbrevs[key]
        except KeyError:
            abbv = self.handle_unknown_event(event, key)
            if not abbv:
                return
        if event.ev_type == 'Key':
            self.old_btn_state[abbv] = self.btn_state[abbv]
            self.btn_state[abbv] = event.state
        if event.ev_type == 'Absolute':
            self.old_abs_state[abbv] = self.abs_state[abbv]
            self.abs_state[abbv] = event.state
        #self.output_state(event.ev_type, abbv)
        self.handle_inputs(event.ev_type, abbv)

    def format_state(self):
        """Format the state."""
        output_string = ""
        for key, value in self.abs_state.items():
            output_string += key + ':' + '{:>4}'.format(str(value) + ' ')

        for key, value in self.btn_state.items():
            output_string += key + ':' + str(value) + ' '

        return output_string

    def output_state(self, ev_type, abbv):
        """Print out the output state."""
        if ev_type == 'Key':
            if self.btn_state[abbv] != self.old_btn_state[abbv]:
                print(self.format_state())
                return

        if abbv[0] == 'H':
            print(self.format_state())
            return

        difference = self.abs_state[abbv] - self.old_abs_state[abbv]
        if (abs(difference)) > MIN_ABS_DIFFERENCE:
            print(self.format_state())

    def handle_mouse(self):
        mouse_move_abs = [0, 0]
        mouse_move_rel = [0, 0]

        # char mouse moves
        for k, v in self.abs_state.items():
            if k == 'LX':
                mouse_move_abs[0] = v - 128
            if k == 'LY':
                mouse_move_abs[1] = v - 128
            if k == 'RX':
                mouse_move_rel[0] = v - 128
            if k == 'RY':
                mouse_move_rel[1] = v - 128

        if abs(mouse_move_rel[0]) > MOVE_THRESHOLD or abs(mouse_move_rel[1]) > MOVE_THRESHOLD:
            self.mouse_mode = 1
        elif abs(mouse_move_abs[0]) > MOVE_THRESHOLD or abs(mouse_move_abs[1]) > MOVE_THRESHOLD:
            self.mouse_mode = 0
            self.mouse.left()

        if self.mouse_mode == 1:
            distance = (mouse_move_rel[0] ** 2 + mouse_move_rel[1] ** 2) ** 0.5
            distance = int(distance * 10 / 128)

            point_diff = move_distance(angle(mouse_move_rel[0], mouse_move_rel[1]), distance=distance)
            self.mouse and self.mouse.move(point_diff[0], point_diff[1], relative=True)
            self.mouse.left(on=self.btn_state.get('TL2') and True or False)
        else:
            distance = (mouse_move_abs[0] ** 2 + mouse_move_abs[1] ** 2) ** 0.5
            distance = int(distance * DISTANCE / 128)

            point_diff = move_distance(angle(mouse_move_abs[0], mouse_move_abs[1]), distance=distance)
            self.mouse and self.mouse.move(SCREEN_X / 2 + point_diff[0], SCREEN_Y / 2 + point_diff[1])

            if abs(mouse_move_abs[0]) < MOVE_THRESHOLD and abs(mouse_move_abs[1]) < MOVE_THRESHOLD:
                self.mouse.left(on=False)

            self.mouse.right(on=self.btn_state.get('TR') and True or False)
            self.mouse.middle(on=self.btn_state.get('TL') and True or False)


    def handle_inputs(self, ev_type, abbv):
        difference = 0

        # BTN
        if ev_type == 'Key':
            if self.btn_state[abbv] == self.old_btn_state[abbv]:
                pass
        elif abbv[0] == 'H':
            if self.abs_state[abbv] == self.old_abs_state[abbv]:
                pass
        else:
            difference = self.abs_state[abbv] - self.old_abs_state[abbv]
            if (abs(difference)) > MIN_ABS_DIFFERENCE:
                print(self.format_state())

        self.handle_mouse()

        # buttons
        keys = []
        if abbv in ('HX', 'HY') and \
                self.abs_state[abbv] != self.old_abs_state[abbv]:
            if not self.btn_state.get('TR3'):
                if abbv == 'HX':
                    if self.abs_state[abbv] == -1:
                        keys.append(KeyCode.KEY_1)
                    if self.abs_state[abbv] == 1:
                        keys.append(KeyCode.KEY_3)
                if abbv == 'HY':
                    if self.abs_state[abbv] == -1:
                        keys.append(KeyCode.KEY_2)
                    if self.abs_state[abbv] == 1:
                        keys.append(KeyCode.KEY_4)
            else:
                if abbv == 'HX':
                    if self.abs_state[abbv] == -1:
                        keys.append(KeyCode.KEY_5)
                    if self.abs_state[abbv] == 1:
                        keys.append(KeyCode.KEY_7)
                if abbv == 'HY':
                    if self.abs_state[abbv] == -1:
                        keys.append(KeyCode.KEY_6)
                    #if self.abs_state[abbv] == 1:
                    #    keys.append(KeyCode.KEY_8)

        #if abbv in ('N', 'E', 'S', 'W') and \
        #        self.btn_state[abbv] != self.old_btn_state[abbv]:
        # these skill button can be hold
        if not self.btn_state.get('TR3'):
            if self.btn_state.get('W') == 1:
                keys.append(KeyCode.KEY_Q)
            if self.btn_state.get('N') == 1:
                keys.append(KeyCode.KEY_W)
            if self.btn_state.get('E') == 1:
                keys.append(KeyCode.KEY_E)
        else:
            if self.btn_state.get('W') == 1:
                self.keyboard.press(KeyCode.KEY_ALT)
            elif self.btn_state.get('W') == 0:
                self.keyboard.press(KeyCode.KEY_ALT, release=True)
            if self.btn_state.get('N') == 1:
                keys.append(KeyCode.KEY_R)
            if self.btn_state.get('E') == 1:
                keys.append(KeyCode.KEY_T)

        # but ESC could check double input
        if abbv == 'S' and self.btn_state[abbv] == 1 and \
                self.btn_state[abbv] != self.old_btn_state[abbv]:
            keys.append(KeyCode.KEY_ESC)

        # but ESC could check double input
        if abbv == 'THR' and self.btn_state[abbv] == 1 and \
                self.btn_state[abbv] != self.old_btn_state[abbv]:
            keys.append(KeyCode.KEY_X)

        self.keyboard.input(keys)

    def process_events(self):
        """Process available events."""
        try:
            events = self.gamepad.read()
        except EOFError:
            events = []
        for event in events:
            self.process_event(event)


def main():
    """Process all events forever."""
    controller = Controller(mouse=UinputMouse(), keyboard=UinputKeyboard())
    while 1:
        controller.process_events()


if __name__ == "__main__":
    main()
