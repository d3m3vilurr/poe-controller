class BaseWindow(object):
    def get_window_size(self):
        return (1920, 1080)

    def get_window_offset(self):
        return (0, 0)

    def get_radius(self):
        return 50

    def is_active(self):
        return True
