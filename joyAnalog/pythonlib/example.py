import joyanalog

switch = joyanalog.joyanalog("COM5", "COM4")
switch.connect()

# switch.button_click(100, 100, ['a'])
# switch.button_click(100, 100, ['b'])
# switch.button_click(100, 100, ['x'])
switch.button_click(100, 100, ['y'])

# switch.button_click(100, 100, ['rs'])
# switch.button_click(100, 100, ['zr'])
# switch.button_click(100, 100, ['rsl'])
# switch.button_click(100, 100, ['rsr'])

# switch.button_click(100, 100, ['+'])
# switch.button_click(100, 100, ['h'])
# switch.button_click(100, 100, ['sbr'])
# switch.button_click(100, 100, ['syncr'])

# switch.reset()
switch.disconnect()