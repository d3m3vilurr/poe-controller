"""Simple gamepad/joystick test example."""

from __future__ import print_function
import uinput
import inputs
from mouse import DefaultMouse
import math
import enum

# TODO get right size from application
SCREEN_X = 1920
SCREEN_Y = 1080
# don't know reason wayland use half
SCREEN_X = 1920 / 2
SCREEN_Y = 1080 / 2

CENTER_X = int(SCREEN_X / 2)
CENTER_Y = int(SCREEN_Y / 2)

DISTANCE = 50

MOVE_THRESHOLD = 20

KEY_INPUT_DELAY = 10

def angle(x, y):
    return math.atan2(y, x)

def move_distance(angle, distance=DISTANCE):
    return int(distance * math.cos(angle)), int(distance * math.sin(angle))

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

    # D-PAD remap
    ('Key-BTN_DL', 'DL'),
    ('Key-BTN_DR', 'DR'),
    ('Key-BTN_DU', 'DU'),
    ('Key-BTN_DD', 'DD'),

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
            mouse = DefaultMouse()
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

    def format_state(self):
        """Format the state."""
        output_string = ""
        for key, value in self.abs_state.items():
            output_string += key + ':' + '{:>4}'.format(str(value) + ' ')

        for key, value in self.btn_state.items():
            output_string += key + ':' + str(value) + ' '

        return output_string

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
            if self.mouse_mode != 0:
                # forceful release all buttons
                self.mouse.left(on=False)
                self.mouse.right(on=False)
                self.mouse.middle(on=False)
            self.mouse_mode = 1
        elif abs(mouse_move_abs[0]) > MOVE_THRESHOLD or abs(mouse_move_abs[1]) > MOVE_THRESHOLD:
            if self.mouse_mode != 0:
                self.mouse_mode = 0
            # forceful activate left mouse
            self.mouse.left()

        if self.mouse_mode == 1:
            distance = (mouse_move_rel[0] ** 2 + mouse_move_rel[1] ** 2) ** 0.5
            distance = int(distance * 10 / 128)

            point_diff = move_distance(angle(mouse_move_rel[0], mouse_move_rel[1]), distance=distance)
            self.mouse.move(point_diff[0], point_diff[1], relative=True)
            self.mouse.left(on=self.pressed('TL2'))
        else:
            distance = (mouse_move_abs[0] ** 2 + mouse_move_abs[1] ** 2) ** 0.5
            distance = int(distance * DISTANCE / 128)

            point_diff = move_distance(angle(mouse_move_abs[0], mouse_move_abs[1]), distance=distance)
            self.mouse.move(CENTER_X + point_diff[0], CENTER_Y + point_diff[1])

            if abs(mouse_move_abs[0]) < MOVE_THRESHOLD and abs(mouse_move_abs[1]) < MOVE_THRESHOLD:
                self.mouse.left(on=False)

            self.mouse.right(on=self.pressed('TR'))
            self.mouse.middle(on=self.pressed('TL'))

    def pressed(self, abbv):
        return self.btn_state.get(abbv, 0) != 0

    def holded(self, abbv):
        return self.btn_state.get(abbv, 0) == self.old_btn_state.get(abbv, 0)

    def handle_inputs(self):
        keys = []
        if not self.pressed('TR3'):
            # DPAD should check button holding
            if self.pressed('DL') and not self.holded('DL'):
                keys.append(KeyCode.KEY_1)
            if self.pressed('DU') and not self.holded('DU'):
                keys.append(KeyCode.KEY_2)
            if self.pressed('DR') and not self.holded('DR'):
                keys.append(KeyCode.KEY_3)
            if self.pressed('DD') and not self.holded('DD'):
                keys.append(KeyCode.KEY_4)
            # Normal button can support firing when holding the button
            if self.pressed('W'):
                keys.append(KeyCode.KEY_Q)
            if self.pressed('N'):
                keys.append(KeyCode.KEY_W)
            if self.pressed('E'):
                keys.append(KeyCode.KEY_E)
        else:
            # DPAD should check button holding
            if self.pressed('DL') and not self.holded('DL'):
                keys.append(KeyCode.KEY_5)
            if self.pressed('DU') and not self.holded('DU'):
                keys.append(KeyCode.KEY_6)
            if self.pressed('DR') and not self.holded('DR'):
                keys.append(KeyCode.KEY_7)
            #if self.pressed('DD') and not self.holded('DD'):
            #    keys.append(KeyCode.KEY_8)
            # Normal button can support firing when holding the button

            # XXX: alt should call press/release manually
            if self.pressed('W'):
                self.keyboard.press(KeyCode.KEY_ALT)
            else:
                self.keyboard.press(KeyCode.KEY_ALT, release=True)
            if self.pressed('N'):
                keys.append(KeyCode.KEY_R)
            if self.pressed('E'):
                keys.append(KeyCode.KEY_T)

        # when press escape key, controller must release button before call it
        if self.pressed('S') and not self.holded('S'):
            keys.append(KeyCode.KEY_ESC)

        if self.pressed('THR') and not self.holded('THR'):
            keys.append(KeyCode.KEY_X)

        difference = 0

        self.handle_mouse()
        #print(keys)
        self.keyboard.input(keys)

    def process_events(self):
        """Process available events."""
        try:
            events = self.gamepad.read()
        except EOFError:
            events = []

        if len(events) == 1 and events[0].ev_type in ('Sync', 'Misc'):
            return

        btn_state = {}
        abs_state = {}

        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.old_abs_state[value] = abs_state[value] = self.abs_state.get(value, 128)
            if key.startswith('Key'):
                self.old_btn_state[value] = btn_state[value] = self.btn_state.get(value, 0)

        for event in events:
            if event.ev_type == 'Misc':
                continue
            key = event.ev_type + '-' + event.code
            try:
                abbv = self.abbrevs[key]
            except KeyError:
                abbv = self.handle_unknown_event(event, key)
                if not abbv:
                    continue
            if event.ev_type == 'Key':
                btn_state[abbv] = event.state
            if event.ev_type == 'Absolute':
                abs_state[abbv] = event.state

                if abbv == 'HX':
                    btn_state['DL'] = btn_state['DR'] = 0
                    if event.state < 0:
                        btn_state['DL'] = 1
                    elif event.state > 0:
                        btn_state['DR'] = 1
                if abbv == 'HY':
                    btn_state['DU'] = btn_state['DD'] = 0
                    if event.state < 0:
                        btn_state['DU'] = 1
                    elif event.state > 0:
                        btn_state['DD'] = 1

        self.btn_state = btn_state
        self.abs_state = abs_state

        #print(self.format_state())
        self.handle_inputs()



def main():
    """Process all events forever."""
    controller = Controller(keyboard=UinputKeyboard())
    while 1:
        controller.process_events()


if __name__ == "__main__":
    main()
