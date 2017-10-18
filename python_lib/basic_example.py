import time
import joyanalog

"""
available button arguments:
["a", "b", "x", "y", "rs", "zr", "+", "h", "rsl", "rsr", "syncr", "sbr"]
["du", "dd", "dl", "dr", "ls", "zl", "-", "cap", "lsl", "lsr", "syncl", "sbl"]
"""

# serial port of two joyanalogs
switch = joyanalog.joyanalog("COM8", "COM4")
switch.connect()

# note the argument is a list
switch.button_hold(['a'])
time.sleep(0.1)
switch.button_release(['a'])

# use this to press button(s) and then release it after a set time
# this has the same effect as the above example, but simpler
# arguments: on_duration_ms, off_duration_ms, button_list
switch.button_click(100, 100, ['a'])

# you can also press multiple buttons at once
switch.button_click(100, 100, ['a', 'du'])

# use this to release all buttons
switch.button_release_all()

# move analog stick to position
# 127 is the netual position for both x and y
# arguments: side('l' or 'r'), x_value(0 to 255), y_value(0 to 255)
switch.stick_hold('l', 127, 211);

# return stick to netural position
switch.stick_release('l')

# move stick to position, hold it for a set time, then return to netural
switch.stick_nudge('r', 100, 100, 0, 127)

switch.disconnect()