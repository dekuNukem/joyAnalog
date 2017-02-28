import sys
import time
import serial
import threading
import switch_ctrl
import irc_bot_noblock
from command_printer import *
from collections import OrderedDict

switch_cmd_map = {
"dup" : [0, "du"],
"ddown" : [1, "dd"],
"dleft" : [2, "dl"],
"dright" : [3, "dr"],
"l" : [4, "ls"],
"zl" : [5, "zl"],
"minus" : [6, "-"],
"cap" : [7, "cap"],
"lsl" : [8, "lsl"],
"lsr" : [9, "lsr"],
"syncl" : [10, "syncl"],
"sbl" : [11, "sbl"],
"a" : [12, "a"],
"b" : [13, "b"],
"x" : [14, "x"],
"y" : [15, "y"],
"r" : [16, "rs"],
"zr" : [17, "zr"],
"plus" : [18, "+"],
"h" : [19, "h"],
"rsl" : [20, "rsl"],
"rsr" : [21, "rsr"],
"syncr" : [22, "syncr"],
"sbr" : [23, "sbr"],
"up" : [24, ""],
"down" : [25, ""],
"left" : [26, ""],
"right" : [27, ""],
"cup" : [28, ""],
"cdown" : [29, ""],
"cleft" : [30, ""],
"cright" : [31, ""]
}

latest_cmd = None
username_color_dict = OrderedDict()

def is_valid_command(command_list):
    if len(command_list) > 3 or len(command_list) <= 0:
        return False
    return True

def execute_cmd(cmd_list):
    global latest_cmd
    button_args = []
    for item in cmd_list:
        if 0 <= switch_cmd_map[item][0] <= 23:
            button_args.append(switch_cmd_map[item][1])
    latest_cmd = (switch.button_click, button_args)
    return

def do_anarchy(chat_username, cmd_list):
    if(is_valid_command(cmd_list)):
        command_printer_in = []
        command_printer_in.append(chat_username)
        command_printer_in.append(cmd_list)
        if chat_username in username_color_dict:
            command_printer_in.append(username_color_dict[chat_username])
        else:
            command_printer_in.append("white")
        print_command_list(command_printer_in, 20, 0)
        execute_cmd(cmd_list)

def safe_print(item):
    try:
        print(item)
    except Exception:
        print(item.encode('utf-8'))

def get_cmd(chat_line):
    try:
        line_split = chat_line.lower().split("+")
        cmd_list = []
        cmd_list_nospace = []
        for item in line_split:
            cmd_list.append(item)
        if len(cmd_list) <= 1:
            cmd_list_nospace = cmd_list
        else:
            for item in cmd_list[:-1]:
                cmd_list_nospace.append(item.replace(" ", ''))
        cmd_list_nospace.append(cmd_list[-1])
        cmd_list_nospace[-1] = cmd_list_nospace[-1].lstrip().split(" ")[0]
        for item in cmd_list_nospace:
            if item not in switch_cmd_map:
                return []
        return list(set(cmd_list_nospace))
    except Exception as e:
        safe_print("get_cmd: " + str(e))
        return []

def worker():
    global latest_cmd
    while 1:
        if latest_cmd != None:
            func = latest_cmd[0]
            arg = latest_cmd[1]
            func(200, arg)
            latest_cmd = None
        time.sleep(0.005)

# if(len(sys.argv) != 2):
#     print ('launch.py <serial port>')
#     sys.exit(0)

switch = switch_ctrl.switch_ctrl("COM4", "COM9")
switch.connect()

nickname = 'STM32F429ZIT6U'
oauth = 'oauth:xj328fatmerr48qqlmkh59onpp6qzc'
chat_channel = 'twitchplayspokemon'
chat_server = ['irc.chat.twitch.tv', 6667]
bot = irc_bot_noblock.irc_bot(nickname, oauth, chat_channel, chat_server[0], chat_server[1], timeout=300, tags = 1)
bot.connect()

t = threading.Thread(target=worker)
t.start()

while 1:
    tmi_list = bot.get_parsed_message()
    tmi_list.reverse()
    for item in [x for x in tmi_list if "." not in x.username]:
        username = item.username
        message_orig = item.message.replace(chr(1) + "ACTION", "").replace(chr(1), '').lstrip().rstrip()
        safe_print(item.username + ": " + message_orig)

        username_color_dict[username] = item.color
        if len(username_color_dict) > 200:
            username_color_dict.popitem(last=False)

        command_list = get_cmd(message_orig)
        do_anarchy(username, command_list)
    user_command_root.update()
    time.sleep(0.01)
