import time
from inputs import get_gamepad
import ctypes
from ctypes import wintypes
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

MOUSEEVENTF_MOVE = 0x0001
ULONG_PTR = wintypes.LPARAM

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

WHEEL_SENSITIVITY = 2
WHEEL_DEADZONE = 3

CROSSFADER_LEFT_THRESHOLD = 10000
CROSSFADER_RIGHT_THRESHOLD = 20000

crossfader_left_pressed = False
crossfader_right_pressed = False

left_click_held = False
euphoria_held = False

buttons_pressed = set()

mouse = MouseController()
keyboard = KeyboardController()

def send_mouse_move(dx):
    """Send relative mouse movement (raw-style) via Windows API."""
    print(f"Moving mouse by {dx}")
    inp = INPUT()
    inp.type = 0
    inp.mi = MOUSEINPUT(dx, 0, 0, MOUSEEVENTF_MOVE, 0, 0)
    SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def process_events():
    global buttons_pressed
    wheel_value = None
    crossfader_value = None

    try:
        events = get_gamepad()
        print("Processing gamepad events")
        for event in events:
            print(f"Event: {event.code}, State: {event.state}, Type: {event.ev_type}")
            if event.code == 'ABS_Y':
                wheel_value = event.state
            elif event.code == 'ABS_Z':
                crossfader_value = event.state
            elif event.ev_type == 'Key':
                if event.state == 1:
                    buttons_pressed.add(event.code)
                    print(f"Button pressed: {event.code}")
                elif event.state == 0:
                    buttons_pressed.discard(event.code)
                    print(f"Button released: {event.code}")
    except Exception as e:
        print(f"Error processing events: {e}")

    return wheel_value, crossfader_value

def main():
    global crossfader_left_pressed, crossfader_right_pressed, left_click_held, euphoria_held, buttons_pressed

    print("Starting DJ to SpinRhythm! Get ready. This is going to be intense..")

    while True:
        try:
            wheel_value, crossfader_value = process_events()

            if wheel_value is not None and abs(wheel_value) > WHEEL_DEADZONE:
                move_amount = int(wheel_value * WHEEL_SENSITIVITY)
                print(f"Wheel value: {wheel_value}, Moving mouse by: {move_amount}")
                send_mouse_move(move_amount)

            if 'BTN_SOUTH' in buttons_pressed:
                if not left_click_held:
                    mouse.press(Button.left)
                    left_click_held = True
                    print("Left mouse button pressed")
            else:
                if left_click_held:
                    mouse.release(Button.left)
                    left_click_held = False
                    print("Left mouse button released")

            if any(btn in buttons_pressed for btn in ['BTN_EAST', 'BTN_WEST']):
                keyboard.press('z')
                print("Z key pressed")
            else:
                keyboard.release('z')
                print("Z key released")

            if 'BTN_NORTH' in buttons_pressed:
                if not euphoria_held:
                    keyboard.press(Key.space)
                    euphoria_held = True
                    print("Space key pressed (Euphoria)")
            else:
                if euphoria_held:
                    keyboard.release(Key.space)
                    euphoria_held = False
                    print("Space key released (Euphoria)")


        except KeyboardInterrupt:
            print("Program terminated by user")
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    main()
    print("Program ended. Press Ctrl+C again to close.")
    try:
        while True:
            time.sleep(1)  # Keep program running until another Ctrl+C
    except KeyboardInterrupt:
        print("Exiting program")