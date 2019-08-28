import sys
import inputs
from .mouse import ButtonCode as MouseButtonCode, DefaultMouse
from .keyboard import KeyCode, DefaultKeyboard
from .window import DefaultWindow
import math
import enum
import time

DISTANCE = 50
MOVE_THRESHOLD = 20

if sys.platform == 'win32':
    ABS_DIV = (256, -256)
    ABS_OFF = 0
else:
    ABS_DIV = (1, 1)
    ABS_OFF = -128

def angle(x, y):
    return math.atan2(y, x)

def move_distance(angle, distance=DISTANCE):
    return int(distance * math.cos(angle)), int(distance * math.sin(angle))


EVENT_ABB = (
    # D-PAD, aka HAT
    ('Absolute-ABS_HAT0X', 'HX'),
    ('Absolute-ABS_HAT0Y', 'HY'),

    # Analogs
    ('Absolute-ABS_X', 'LX'),
    ('Absolute-ABS_Y', 'LY'),
    ('Absolute-ABS_Z', 'LZ'),
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
    ('Key-BTN_TR2', 'TR2'),
    ('Key-BTN_MODE', 'M'),
    ('Key-BTN_START', 'ST'),
    ('Key-BTN_SELECT', 'SL'),

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
    def __init__(self, gamepad=None, window=None, keyboard=None, mouse=None, abbrevs=EVENT_ABB):
        self.btn_state = {}
        self.old_btn_state = {}
        self.abs_state = {}
        self.old_abs_state = {}
        self.abbrevs = dict(abbrevs)
        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.abs_state[value] = 0
                self.old_abs_state[value] = 0
            if key.startswith('Key'):
                self.btn_state[value] = 0
                self.old_btn_state[value] = 0
        self._other = 0
        self.gamepad = gamepad
        if not gamepad:
            self._get_gamepad()
        if not window:
            window = DefaultWindow()
        if not mouse:
            mouse = DefaultMouse()
        if not keyboard:
            keyboard = DefaultKeyboard()
        self.window = window
        self.mouse = mouse
        self.keyboard = keyboard
        self.mouse_mode = 0
        self.key_pressed = set()
        self.mouse_pressed = set()

    def _get_gamepad(self):
        """Get a gamepad object."""
        try:
            devices = inputs.DeviceManager()
            self.gamepad = devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError('No gamepad found.')

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
        mouse_presses = set()
        mouse_move_abs = [0, 0]
        mouse_move_rel = [0, 0]

        # char mouse moves
        for k, v in self.abs_state.items():
            if k == 'LX':
                mouse_move_abs[0] = v
            if k == 'LY':
                mouse_move_abs[1] = v
            if k == 'RX':
                mouse_move_rel[0] = v
            if k == 'RY':
                mouse_move_rel[1] = v

        if abs(mouse_move_rel[0]) > MOVE_THRESHOLD or abs(mouse_move_rel[1]) > MOVE_THRESHOLD:
            self.mouse_mode = 1
        elif abs(mouse_move_abs[0]) > MOVE_THRESHOLD or abs(mouse_move_abs[1]) > MOVE_THRESHOLD:
            if self.mouse_mode != 0:
                self.mouse_mode = 0
            # forceful activate left mouse
            mouse_presses.add(MouseButtonCode.LEFT)

        if self.mouse_mode == 1:
            distance = (mouse_move_rel[0] ** 2 + mouse_move_rel[1] ** 2) ** 0.5
            distance = int(distance * 10 / 128)

            point_diff = move_distance(angle(mouse_move_rel[0], mouse_move_rel[1]), distance=distance)
            self.mouse.move(point_diff[0], point_diff[1], relative=True)
        else:
            distance = (mouse_move_abs[0] ** 2 + mouse_move_abs[1] ** 2) ** 0.5
            # left / right should move to twice than up / down
            distance = int(distance * self.window.get_radius() / 128)

            point_diff = move_distance(angle(mouse_move_abs[0], mouse_move_abs[1]), distance=distance)

            win_size = self.window.get_window_size()
            win_offset = self.window.get_window_offset()

            cursor_x = int((win_size[0] / 2) + point_diff[0] + win_offset[0])
            cursor_y = int((win_size[1] / 2) + point_diff[1] + win_offset[1])
            self.mouse.move(cursor_x, cursor_y)
        return mouse_presses

    def pressed(self, abbv):
        return self.btn_state.get(abbv, 0) != 0

    def holded(self, abbv):
        return self.btn_state.get(abbv, 0) == self.old_btn_state.get(abbv, 0)

    def handle_inputs(self):
        key_presses = set()
        key_clicks = set()
        mouse_presses = set()
        # Flasks (L1, Left, Up, Right, R1)
        if self.pressed('TL') and not self.holded('TL'):
            key_clicks.add(KeyCode.KEY_1)
        if self.pressed('DL') and not self.holded('DL'):
            key_clicks.add(KeyCode.KEY_2)
        if self.pressed('DU') and not self.holded('DU'):
            key_clicks.add(KeyCode.KEY_3)
        if self.pressed('DR') and not self.holded('DR'):
            key_clicks.add(KeyCode.KEY_4)
        if self.pressed('TR') and not self.holded('TR'):
            key_clicks.add(KeyCode.KEY_5)

        if self.pressed('TR2'):
            # Toggle loot filter (R2 + L3)
            if self.pressed('THL') and not self.holded('THL'):
                key_clicks.add(KeyCode.KEY_Z)
            # Swap weapon (R2 + R3)
            if self.pressed('THR') and not self.holded('THR'):
                key_clicks.add(KeyCode.KEY_X)
            # Show dropped items (R2 + Down)
            if self.pressed('DD'):
                key_presses.add(KeyCode.KEY_ALT)

        # when holding TR2 use second skill set
        if self.pressed('TR2'):
            if self.pressed('W'):
                key_presses.add(KeyCode.KEY_Q)
            if self.pressed('N'):
                mouse_presses.add(MouseButtonCode.LEFT)
            if self.pressed('E'):
                mouse_presses.add(MouseButtonCode.MIDDLE)
            if self.pressed('S'):
                mouse_presses.add(MouseButtonCode.RIGHT)
        else:
            if self.pressed('W'):
                key_presses.add(KeyCode.KEY_W)
            if self.pressed('N'):
                key_presses.add(KeyCode.KEY_E)
            if self.pressed('E'):
                key_presses.add(KeyCode.KEY_R)
            if self.pressed('S'):
                key_presses.add(KeyCode.KEY_T)

        if self.pressed('TL2'):
            # Hold current position if doesn't use moving without attack (L2)
            self.pressed(KeyCode.KEY_SHIFT)

            if self.pressed('THL') and not self.holded('THL'):
                pass
            if self.pressed('THR') and not self.holded('THR'):
                pass
            if self.pressed('DD') and not self.holded('DD'):
                pass

        if not self.pressed('TL2') and not self.pressed('TR2'):
            # Toggle mini map (Down)
            if self.pressed('DD') and not self.holded('DD'):
                self.pressed(KeyCode.KEY_TAB)

        # when press escape key, controller must release button before call it
        if self.pressed('ST') and not self.holded('ST'):
            key_clicks.add(KeyCode.KEY_ESC)

        if self.pressed('SL') and not self.holded('SL'):
            key_clicks.add(KeyCode.KEY_I)


        difference = 0

        mouse_presses |= self.handle_mouse()
        self.mouse.releases(self.mouse_pressed - mouse_presses)
        self.mouse.presses(mouse_presses - self.mouse_pressed)
        self.mouse_pressed = mouse_presses
        self.keyboard.clicks(key_clicks)
        self.keyboard.releases(self.key_pressed - key_presses)
        self.keyboard.presses(key_presses - self.key_pressed)
        self.key_pressed = key_presses


    def process_events(self):
        """Process available events."""
        events = []
        while True:
            try:
                new_events = self.gamepad.read()
            except EOFError:
                pass
            events += new_events
            if any((ev.ev_type == 'Sync' for ev in new_events)):
                break

        #print(tuple(ev.ev_type for ev in events))

        btn_state = {}
        abs_state = {}

        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.old_abs_state[value] = abs_state[value] = self.abs_state.get(value, 0)
            elif key.startswith('Key'):
                self.old_btn_state[value] = btn_state[value] = self.btn_state.get(value, 0)

        for event in events:
            if event.ev_type == 'Sync':
                continue
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
            elif event.ev_type == 'Absolute':
                abs_state[abbv] = event.state

                if abbv == 'HX':
                    btn_state['DL'] = btn_state['DR'] = 0
                    if event.state < 0:
                        btn_state['DL'] = 1
                    elif event.state > 0:
                        btn_state['DR'] = 1
                elif abbv == 'HY':
                    btn_state['DU'] = btn_state['DD'] = 0
                    if event.state < 0:
                        btn_state['DU'] = 1
                    elif event.state > 0:
                        btn_state['DD'] = 1
                elif abbv in ('LX', 'RX'):
                    abs_state[abbv] = int(abs_state[abbv] / ABS_DIV[0]) + ABS_OFF
                elif abbv in ('LY', 'RY'):
                    abs_state[abbv] = int(abs_state[abbv] / ABS_DIV[1]) + ABS_OFF
        btn_state['TL2'] = abs_state['LZ'] == 255 and 1 or 0
        btn_state['TR2'] = abs_state['RZ'] == 255 and 1 or 0

        self.btn_state = btn_state
        self.abs_state = abs_state

        #print(self.format_state())

        if self.window.is_active():
            self.handle_inputs()
