import joyanalog

switch = joyanalog.joyanalog("COM8", "COM4")
switch.connect()

# switch.button_click(100, 100, ['a'])
# switch.button_click(100, 100, ['b'])
# switch.button_click(100, 100, ['x'])
# switch.button_click(100, 100, ['y'])

# switch.button_click(100, 100, ['rs'])
# switch.button_click(100, 100, ['zr'])
# switch.button_click(100, 100, ['rsl'])
# switch.button_click(100, 100, ['rsr'])

# switch.button_click(100, 100, ['+'])
# switch.button_click(100, 100, ['h'])
# switch.button_click(100, 100, ['sbr'])

switch.button_click(100, 100, ['du'])
switch.button_click(100, 100, ['dd'])
switch.button_click(100, 100, ['dl'])
switch.button_click(100, 100, ['dr'])

switch.button_click(100, 100, ['ls'])
switch.button_click(100, 100, ['zl'])
switch.button_click(100, 100, ['lsl'])
switch.button_click(100, 100, ['lsr'])

switch.button_click(100, 100, ['-'])
switch.button_click(100, 100, ['sbl'])
switch.button_click(100, 100, ['cap'])


switch.disconnect()