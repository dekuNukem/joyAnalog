import os
import sys
import time
import serial
import random
# import switch_ctrl
import irc_bot_noblock
from command_printer import *
from collections import OrderedDict

def current_time_sec():
    return int(time.time())

def current_time_float():
    return time.time()

main_directional_control = "dpad"
buttonpress_delay = 0.2

username_color_dict = OrderedDict()
cpad_up = 'ch 140 255\n'
cpad_down = 'ch 140 0\n'
cpad_left = 'ch 255 140\n'
cpad_right = 'ch 0 140\n'
dpad_up = 'bh u\n'
dpad_down = 'bh d\n'
dpad_left = 'bh l\n'
dpad_right = 'bh r\n'

def is_valid_command(command_list):
    if len(command_list) > 3 or len(command_list) <= 0:
        return False

    if("up" in command_list and "down" in command_list) or\
    ("left" in command_list and "right" in command_list) or\
    ("a" in command_list and "b" in command_list) or\
    ("x" in command_list and "y" in command_list) or\
    ("l" in command_list and "r" in command_list) or\
    ("start" in command_list and "select" in command_list):
        return False
    return True

def roll_random(probability):
    if(probability >= 1):
        return True
    if(probability <= 0):
        return False
    return random.random() < probability

def press(chat_username, command_list, admin_override = False, touch_delay = 0.1):
    global buttonpress_delay
    global next_release

    try:
        for item in command_list:
            if button_enabled or admin_override:
                if item == "a" :
                    ser.write(('bh a\n').encode())
                elif item == "b" :
                    ser.write(('bh b\n').encode())
                elif item == "x" :
                    ser.write(('bh x\n').encode())
                elif item == "y" :
                    ser.write(('bh y\n').encode())

                elif main_directional_control == "cpad":
                    if item == "up":
                        ser.write(cpad_up.encode())
                    elif item == "down":
                        ser.write(cpad_down.encode())
                    elif item == "left":
                        ser.write(cpad_left.encode())
                    elif item == "right":
                        ser.write(cpad_right.encode())
                    elif item == "dup":
                        ser.write(dpad_up.encode())
                    elif item == "ddown":
                        ser.write(dpad_down.encode())
                    elif item == "dleft":
                        ser.write(dpad_left.encode())
                    elif item == "dright":
                        ser.write(dpad_right.encode())

                elif main_directional_control == "dpad":
                    if item == "up":
                        ser.write(dpad_up.encode())
                    elif item == "down":
                        ser.write(dpad_down.encode())
                    elif item == "left":
                        ser.write(dpad_left.encode())
                    elif item == "right":
                        ser.write(dpad_right.encode())
                    elif item == "cup":
                        ser.write(cpad_up.encode())
                    elif item == "cdown":
                        ser.write(cpad_down.encode())
                    elif item == "cleft":
                        ser.write(cpad_left.encode())
                    elif item == "cright":
                        ser.write(cpad_right.encode())

                elif item == "l":
                    ser.write(('bh ls\n').encode())
                elif item == "r":
                    ser.write(('bh rs\n').encode())
                elif item == "start":
                    ser.write(('bh st\n').encode())
                elif item == "select":
                    ser.write(('bh se\n').encode())
                elif item == "home":
                    ser.write(('bh h\n').encode())

        for item in command_list:
            if touch_enabled or admin_override:
                coord_list = str.split(item, ',')
                if len(coord_list) == 2 :
                    x = int(coord_list[0])
                    y = int(coord_list[1])
                    if touch_delay > 0.1:
                        touch_delay = 0.1
                    delay_cmd = "td " + str(int(touch_delay * 1000)) + "\n"
                    if(touch_delay != 0.1):
                        print("=====new touchscreen delay: " + str(delay_cmd))
                    cmd = "tc " + str(x) + " " + str(y) + "\n"
                    ser.write(delay_cmd.encode())
                    ser.write(cmd.encode())
                    overlay_x = (x/320)*crosshair_overlay_width
                    overlay_y = (y/240)*crosshair_overlay_height
                    canvas.create_image(overlay_x, overlay_y, image = crosshair)
                    canvas.update()
                    touch_crosshair_root.update()
    except:
        reset_serial()
    next_release = current_time_float() + buttonpress_delay

def do_anarchy(chat_username, cmd_list):
    global next_release
    if(is_valid_command(cmd_list)):
        command_printer_in = []
        command_printer_in.append(chat_username)
        command_printer_in.append(cmd_list)
        if chat_username in username_color_dict:
            command_printer_in.append(username_color_dict[chat_username])
        else:
            command_printer_in.append("white")
        print_command_list(command_printer_in, 20, 0)
        # diff = buttonpress_delay - (next_release - current_time_float())
        # td = 0.0
        # # diff is how long until the schduled release
        # print(diff)
        # if diff < 0.2:
        #   print("======early release: " + str(diff) + "======")
        #   release_control()
        #   td = diff
        # else:
        #   td = 0.1
        # press(chat_username, cmd_list, touch_delay = td)

def safe_print(item):
    try:
        print(item)
    except Exception:
        print(item.encode('utf-8'))

if(len(sys.argv) != 2):
    print ('launch.py <serial port>')
    sys.exit(0)

nickname = 'twitch_plays_3ds'
oauth = ''
chat_channel = 'twitchplayspokemon'
chat_server = ['irc.chat.twitch.tv', 6667]
bot = irc_bot_noblock.irc_bot(nickname, oauth, chat_channel, chat_server[0], chat_server[1], timeout=300, tags = 1)
bot.connect()

while 1:
    tmi_list = bot.get_parsed_message()
    tmi_list.reverse()
    for item in [x for x in tmi_list if "." not in x.username]:
        username = item.username
        message_orig = item.message.replace(chr(1) + "ACTION", "/me").replace(chr(1), '').lstrip().rstrip()
        safe_print(item.username + ": " + message_orig)

        username_color_dict[username] = item.color
        if len(username_color_dict) > 50:
            username_color_dict.popitem(last=False)

        message_split_list = list(set(message_orig.replace(" ", "").lower().split("+")))
        do_anarchy(username, message_split_list)
    user_command_root.update()
    time.sleep(0.01)
