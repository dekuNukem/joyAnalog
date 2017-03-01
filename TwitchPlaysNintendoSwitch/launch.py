import sys
import time
import serial
import threading
import ndacmini
import irc_bot_noblock
from command_printer import *
from collections import OrderedDict

switch_cmd_map = {
"dup" : "du",
"ddown" : "dd",
"dleft" : "dl",
"dright" : "dr",
"l" : "ls",
"zl" : "zl",
"minus" : "-",
"cap" : "cap",
"lsl" : "lsl",
"lsr" : "lsr",
"syncl" : "syncl",
"sbl" : "sbl",
"a" : "a",
"b" : "b",
"x" : "x",
"y" : "y",
"r" : "rs",
"zr" : "zr",
"plus" : "+",
"h" : "h",
"rsl" : "rsl",
"rsr" : "rsr",
"syncr" : "syncr",
"sbr" : "sbr",
"up": "",
"down": "",
"left": "",
"right": "",
"cup": "",
"cdown": "",
"cleft": "",
"cright": "",
}

latest_cmd = None
username_color_dict = OrderedDict()

def get_list(filename):
    ret = []
    try:
        with open(filename, 'r') as fp:
            for line in fp:
                line = line.lower().replace('\n', '').replace('\r', '').lstrip().rstrip()
                if len(line) <= 0 or line[0] == ';' or line in ret:
                    continue
                ret.append(line)
    except Exception as e:
        print("get_list: " + str(e))
    return ret

def execute_cmd(cmd_list):
    global latest_cmd
    button_list = []
    left_tuple = None
    right_tuple = None
    for item in cmd_list:
        if item == 'up':
            left_tuple = (128, 255)
        elif item == 'down':
            left_tuple = (128, 0)
        elif item == 'left':
            left_tuple = (0, 128)
        elif item == 'right':
            left_tuple = (255, 128)
        elif item == 'cup':
            right_tuple = (128, 255)
        elif item == 'cdown':
            right_tuple = (128, 0)
        elif item == 'cleft':
            right_tuple = (0, 128)
        elif item == 'cright':
            right_tuple = (255, 128)
        elif item in switch_cmd_map:
            button_list.append(switch_cmd_map[item])
    latest_cmd = (button_list, left_tuple, right_tuple)

def is_valid_command(command_list, username):
    if len(command_list) > 3 or len(command_list) <= 0:
        return False
    if username in banned_user:
        print(username + ' is banned!')
        return False
    for item in command_list:
        if item in disabled_cmd:
            print(item + ' is disabled!')
            return False
    return True

def do_anarchy(chat_username, cmd_list):
    if(is_valid_command(cmd_list, chat_username)):
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
            switch.button_stick_ctrl(100, 67, latest_cmd[0], latest_cmd[1], latest_cmd[2])
            latest_cmd = None
        time.sleep(0.005)

# if(len(sys.argv) != 3):
#     print ('launch.py port1 port2')
#     sys.exit(0)

disabled_cmd = get_list("disabled_cmd.txt")
banned_user = get_list("banned_user.txt")

switch = ndacmini.ndacmini("COM4", "COM8")
switch.connect()

nickname = 'STM32F429ZIT6U'
oauth = 'oauth:xj328fatmerr48qqlmkh59onpp6qzc'
chat_channel = 'twitchplayspokemon'
chat_server = ['irc.chat.twitch.tv', 6667]
bot = irc_bot_noblock.irc_bot(nickname, oauth, chat_channel, chat_server[0], chat_server[1], timeout=300, tags = 1)
bot.connect()

t = threading.Thread(target=worker)
t.start()

try:
    while 1:
        tmi_list = bot.get_parsed_message()
        for item in [x for x in tmi_list if "." not in x.username]:
            disabled_cmd = get_list("disabled_cmd.txt")
            banned_user = get_list("banned_user.txt")

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

except KeyboardInterrupt:
    switch.disconnect()
    exit()