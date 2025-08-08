from inputs import get_gamepad

print("Listening for gamepad events. Press buttons or spin platter...")

while True:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
