import time
import threading
from inputs import get_gamepad

next_send = 0

joycon_status = {
    "a" : 0,
    "b" : 0,
    "x" : 0,
    "y" : 0,
    "rs" : 0,
    "zr" : 0,
    "+" : 0,
    "h" : 0,
    "rsl" : 0,
    "rsr" : 0,
    "syncr" : 0,
    "sbr" : 0,

    "du" : 0,
    "dd" : 0,
    "dl" : 0,
    "dr" : 0,
    "ls" : 0,
    "zl" : 0,
    "-" : 0,
    "cap" : 0,
    "lsl" : 0,
    "lsr" : 0,
    "syncl" : 0,
    "sbl" : 0,

    "lx" : 127,
    "ly" : 127,
    "rx" : 127,
    "ry" : 127
}

def worker():
    global next_send
    while 1:
        now = time.time()
        if now <= next_send:
            continue
        # print(joycon_status)
        print(now)
        next_send = now + 0.005

t = threading.Thread(target=worker)
t.start()

while 1:
    for event in get_gamepad():
        if "SNYC" in event.ev_type:
            continue

        # print(str(time.time()) + ' ' + event.code)


        # xbox dpad x
        if event.code == "ABS_HAT0X":
            if event.state == -1:   # left
                joycon_status['dl'] = 1
            elif event.state == 1:  # right
                joycon_status['dr'] = 1
            else:
                joycon_status['dl'] = 0
                joycon_status['dr'] = 0

        # xbox dpad y
        if event.code == "ABS_HAT0Y":
            if event.state == -1:   # left
                joycon_status['du'] = 1
            elif event.state == 1:  # right
                joycon_status['dd'] = 1
            else:
                joycon_status['du'] = 0
                joycon_status['dd'] = 0


        if event.code == "BTN_TL":
            joycon_status['ls'] = event.state

        if event.code == "BTN_TR":
            joycon_status['rs'] = event.state

        if event.code == "BTN_NORTH":
            joycon_status['x'] = event.state

        if event.code == "BTN_SOUTH":
            joycon_status['b'] = event.state

        if event.code == "BTN_WEST":
            joycon_status['y'] = event.state

        if event.code == "BTN_EAST":
            joycon_status['a'] = event.state

        if event.code == "BTN_START":
            joycon_status['-'] = event.state

        if event.code == "BTN_SELECT":
            joycon_status['+'] = event.state

        if event.code == "BTN_THUMBL":
            joycon_status['sbl'] = event.state

        if event.code == "BTN_THUMBR":
            joycon_status['sbr'] = event.state

        if event.code == "ABS_RZ":
            joycon_status['zr'] = event.state

        if event.code == "ABS_Z":
            joycon_status['zl'] = event.state

        if "ABS_X" in event.code:
            joycon_status['lx'] = int((32768 + event.state) / 256)

        if "ABS_Y" in event.code:
            joycon_status['ly'] = int((32768 + event.state) / 256)

        if "ABS_RX" in event.code:
            joycon_status['rx'] = int((32768 + event.state) / 256)

        if "ABS_RY" in event.code:
            joycon_status['ry'] = int((32768 + event.state) / 256)
