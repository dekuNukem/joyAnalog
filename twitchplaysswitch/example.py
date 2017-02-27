import time
import switch_ctrl

def sleep_ms(delay_ms):
    time.sleep(float(delay_ms)/1000)

"""
buttons:
arg       meaning
-----------------------
a       A button
b       B button
x       X button
y       Y button
du      d-pad up
dd      d-pad down
dl      d-pad left
dr      d-pad right
ls      left shoulder
rs      right shoulder
zl		ZL button
zr		ZR button
sl 		SL button
sr 		SR button		
sbl 	left joycon stick button
sbr		right joycon stick button
syncl	left joycon sync button
syncr	right joycon sync button
+		plus button
-		minus button
h 		home button
cap 	capture button

analog sticks:
X: 0 Right, 127 Neutral, 255 Left
Y: 0 Down, 127 Neutral, 255 Up
"""

switch = switch_ctrl.switch_ctrl("COM5")
switch.connect()
switch.release_all()

try:
	while 1:
		# switch.button_click("dd", 50)
		switch.stick_nudge(64, 255, 50)
		# switch.stick_hold(255, 255)
		# switch.release_all()
		sleep_ms(100)
except KeyboardInterrupt:
	switch.release_all()