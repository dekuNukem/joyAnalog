import ndacmini

switch = ndacmini.ndacmini("COM5", "COM6")
switch.connect()

# give it a list of valid button args
switch.button_hold(['a', 'b', 'zl', 'zr'])
switch.button_release(['du'])
switch.button_release_all()

# press button(s) then release it
# first arg is how long to press the button(s) down
# second arg is how long to release them before the next action
# value smaller than 33ms (1 frame) probably won't get recognized by the console
# third arg is the list of buttons
switch.button_click(67, 67, ['+', '-', 'h'])

# first arg is which stick to hold, should be 'l' or 'r'
# second and third arg are desired stick position
# must between 0 to 255 inclusive, 127 is netural postion
switch.stick_hold('l', 64, 192)
switch.stick_release('r')

# give back stick control to user
switch.stick_disengage('l')

# hold the stick to a position then release it
# first arg is which side, should be 'l' or 'r'
# second arg is how long to hold the stick
# third arg is how long to release the stick before the next action
# fourth and fifth arg are stick position x and y
switch.stick_nudge('l', 67, 67, 192, 168)

# release all buttons and disengage all sticks
switch.reset()

switch.disconnect()