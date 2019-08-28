import sys
import time
import inputs
import traceback
from poe_controller import Controller

while 1:
    try:
        controller = Controller()
        while 1:
            controller.process_events()
    except inputs.UnpluggedError:
        pass
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        traceback.print_exc()
    time.sleep(0.1)
