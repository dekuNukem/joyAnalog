import time
import switch_ctrl

def sleep_ms(delay_ms):
    time.sleep(float(delay_ms)/1000)

switch = switch_ctrl.switch_ctrl("COM4", "COM8")
switch.connect()

try:
	while 1:
		switch.button_click(100, ["du", "ls", "zl", "rs", "zr", "+"])
except KeyboardInterrupt:
	switch.disconnect()
