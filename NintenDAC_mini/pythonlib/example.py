import time
import ndacmini

def sleep_ms(delay_ms):
    time.sleep(float(delay_ms)/1000)

switch = ndacmini.ndacmini("COM4", "COM8")
switch.connect()

try:
	while 1:
		switch.button_click(100, ["du", "ls", "zl", "rs", "zr", "+"])
		# switch.stick_nudge('l', 100, 45, 67)
		# switch.stick_hold('l', 45, 67)
		# switch.button_stick_ctrl(100, 67, ["du", "ls", "zl", "rs", "zr", "+"], (23,45), (67,89))
except KeyboardInterrupt:
	switch.disconnect()
