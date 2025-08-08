import hid

def find_dj_hero_device():
    for device in hid.enumerate():
        name = (device['product_string'] or "").lower()
        if "dj" in name or "hero" in name or "xbox" in name:
            return device['vendor_id'], device['product_id'], device['product_string']
    return None, None, None

vid, pid, name = find_dj_hero_device()

if not vid or not pid:
    print("DJ Hero deck not found. Make sure it’s plugged in.")
    exit()

print(f"Found device: {name} (VID={hex(vid)}, PID={hex(pid)})")

try:
    dev = hid.device()
    dev.open(vid, pid)
    dev.set_nonblocking(True)

    print("Listening for HID reports... (Ctrl+C to stop)")
    while True:
        data = dev.read(64)
        if data:
            print(data)

except Exception as e:
    print("Error:", e)
