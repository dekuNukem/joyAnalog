import time
import joyanalog
import threading
import collections
from inputs import get_gamepad

joycon_status = collections.OrderedDict()

joycon_status["l0"] = 0 #0
joycon_status["l1"] = 0
joycon_status["lx"] = 127
joycon_status["ly"] = 127
joycon_status["-"] = 0
joycon_status["sbl"] = 0
joycon_status["cap"] = 0
joycon_status["syncl"] = 0
joycon_status["dd"] = 0
joycon_status["du"] = 0
joycon_status["dr"] = 0
joycon_status["dl"] = 0
joycon_status["lsr"] = 0
joycon_status["lsl"] = 0
joycon_status["ls"] = 0
joycon_status["zl"] = 0 #15

joycon_status["r0"] = 0 #16
joycon_status["r1"] = 0
joycon_status["rx"] = 127
joycon_status["ry"] = 127
joycon_status["+"] = 0
joycon_status["sbr"] = 0
joycon_status["h"] = 0
joycon_status["syncr"] = 0
joycon_status["y"] = 0
joycon_status["x"] = 0
joycon_status["b"] = 0
joycon_status["a"] = 0
joycon_status["rsr"] = 0
joycon_status["rsl"] = 0
joycon_status["rs"] = 0
joycon_status["zr"] = 0 #31

def dump_str():
    ret = ''
    for k, v in joycon_status.items():
        ret += str(v) + ","
    return ret[:-1]

def worker():
    global next_send
    while 1:
        now = time.time()
        ts = now - record_start
        if now <= next_send:
            continue
        message = str(ts)[:8] + "," + dump_str() + "\n"
        switch.tas_ctrl(joycon_status)
        next_send = now + 0.005

switch = joyanalog.joyanalog("COM5", "COM10")
switch.connect()
switch.reset()
next_send = 0
record_start = time.time()
t = threading.Thread(target=worker)
t.start()

while 1:
    for event in get_gamepad():
        if "SNYC" in event.ev_type:
            continue
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
            joycon_status['zr'] = int(event.state > 64)

        if event.code == "ABS_Z":
            joycon_status['zl'] = int(event.state > 64)

        if "ABS_X" in event.code:
            joycon_status['ly'] = int((32768 + event.state) / 256)

        if "ABS_Y" in event.code:
            joycon_status['lx'] = 255 - int((32768 + event.state) / 256)

        if "ABS_RX" in event.code:
            joycon_status['ry'] = 255 - int((32768 + event.state) / 256)

        if "ABS_RY" in event.code:
            joycon_status['rx'] = int((32768 + event.state) / 256)
