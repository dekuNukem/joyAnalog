# read and store button change, push to joyanalog every 5ms

import time
import joyanalog
from inputs import get_gamepad

def bt_ctrl(button_list, state):
	if state == 1:
		switch.button_hold(button_list)
	else:
		switch.button_release(button_list)

lx_value = 127
ly_value = 127
rx_value = 127
ry_value = 127

switch = joyanalog.joyanalog("COM5", "COM7")
switch.connect()

while 1:
	for event in get_gamepad():
		if "sync" in event.ev_type.lower():
			continue

		# if "ABS_" not in event.code:
		# 	print(event.ev_type)
		# 	print(event.code)
		# 	print(event.state)
		# 	print()

		# xbox dpad x
		if event.code == "ABS_HAT0X":
			if event.state == -1:	# left
				switch.button_hold(['dl'])
			elif event.state == 1:	# right
				switch.button_hold(['dr'])
			else:
				switch.button_release(['dl', 'dr'])

		# xbox dpad y
		if event.code == "ABS_HAT0Y":
			if event.state == -1:	# left
				switch.button_hold(['du'])
			elif event.state == 1:	# right
				switch.button_hold(['dd'])
			else:
				switch.button_release(['du', 'dd'])


		if event.code == "BTN_TL":
			bt_ctrl(['ls'], event.state)

		if event.code == "BTN_TR":
			bt_ctrl(['rs'], event.state)

		if event.code == "BTN_NORTH":
			bt_ctrl(['x'], event.state)

		if event.code == "BTN_SOUTH":
			bt_ctrl(['b'], event.state)

		if event.code == "BTN_WEST":
			bt_ctrl(['y'], event.state)

		if event.code == "BTN_EAST":
			bt_ctrl(['a'], event.state)

		if event.code == "BTN_START":
			bt_ctrl(['-'], event.state)

		if event.code == "BTN_SELECT":
			bt_ctrl(['+'], event.state)

		if event.code == "BTN_THUMBL":
			bt_ctrl(['sbl'], event.state)

		if event.code == "BTN_THUMBR":
			bt_ctrl(['sbr'], event.state)

		if event.code == "ABS_RZ":
			bt_ctrl(['zr'], event.state > 64)

		if event.code == "ABS_Z":
			bt_ctrl(['zl'], event.state > 64)

		if "ABS_X" in event.code:
			lx_value = int((32768 + event.state) / 256)

		if "ABS_Y" in event.code:
			ly_value = int((32768 + event.state) / 256)

		if "ABS_RX" in event.code:
			rx_value = int((32768 + event.state) / 256)

		if "ABS_RY" in event.code:
			ry_value = int((32768 + event.state) / 256)

		if "ABS_R" in event.code:
			switch.stick_hold('r', ry_value, 255 - rx_value)

		if "ABS_" in event.code:
			switch.stick_hold('l', 255 - ly_value, lx_value)