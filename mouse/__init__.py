import os

if os.environ.get('WAYLAND_DISPLAY'):
    from mouse.uinput import UinputMouse as DefaultMouse
else:
    from mouse.base import BaseMouse as DefaultMouse
