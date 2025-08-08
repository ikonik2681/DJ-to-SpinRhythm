import time
from inputs import get_gamepad
import ctypes
from ctypes import wintypes

# --- Windows constants ---
MOUSEEVENTF_MOVE = 0x0001

ULONG_PTR = wintypes.LPARAM  # This is pointer-sized

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR)]

class INPUT(ctypes.Structure):
    class _I(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("i",)
    _fields_ = [("type", wintypes.DWORD),
                ("i", _I)]

SendInput = ctypes.windll.user32.SendInput

# Here you can change the sensitivity of your DJ Hero Platter.
WHEEL_SENSITIVITY = 1.5
WHEEL_DEADZONE = 3

def send_mouse_move(dx):
    """Send relative mouse movement (raw-style)."""
    inp = INPUT()
    inp.type = 0  # INPUT_MOUSE
    inp.mi = MOUSEINPUT(dx, 0, 0, MOUSEEVENTF_MOVE, 0, 0)
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def process_events():
    wheel_value = None
    events = get_gamepad()
    for event in events:
        if event.code == 'ABS_Y':  # Platter axis
            wheel_value = event.state
    return wheel_value

def main():
    print("DJ Hero platter → Raw mouse movement started.")
    while True:
        wheel_value = process_events()

        if wheel_value is not None and abs(wheel_value) > WHEEL_DEADZONE:
            move_amount = int(wheel_value * WHEEL_SENSITIVITY)
            send_mouse_move(move_amount)

        time.sleep(0.005)

if __name__ == "__main__":
    main()
