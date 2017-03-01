import time
from tkinter import *
from collections import deque

user_command_root = Tk()

user_command_root.title("TP3DS User Command")
user_command_root.geometry('350x640')
user_command_root.configure(background='black')
user_command_root.resizable(width=FALSE, height=FALSE)
text_font = ("", "20")

command_window_height_lines = 20
username_width_chars = 18
command_width_chars = 200

text_username = Text(user_command_root, height=command_window_height_lines, width=username_width_chars, background = "black", foreground = "white", font = text_font)
text_username.pack()
text_username.place(x=0, y=0)

text_commands = Text(user_command_root, height=command_window_height_lines, width=command_width_chars, background = "black", foreground = "white", font = text_font)
text_commands.pack()
text_commands.place(x=250, y=0)

command_print_queue = deque()
username_print_queue = deque()
color_print_queue = deque()

def make_tag(line_number, position):
	return str(line_number) + "." + str(position)

def replace_arrows(cmd):
	return cmd.replace("up", "↑").replace("down", "↓").replace("left", "←").replace("right", "→")

def print_command_list(command_printer_in, command_length, offset):
	chat_username = command_printer_in[0]
	command_list = command_printer_in[1]
	command_color = command_printer_in[2]

	if len(command_list) == 0 or len(chat_username) == 0:
		return

	user_command = ""
	for item in command_list:
		user_command += item
	user_command = replace_arrows(user_command)

	username_print_queue.append(chat_username[:21].capitalize())
	if(len(username_print_queue) > command_length - offset):
		username_print_queue.popleft()

	command_print_queue.append(user_command[:12])
	if(len(command_print_queue) > command_length - offset):
		command_print_queue.popleft()

	color_print_queue.append(command_color)
	if(len(color_print_queue) > command_length - offset):
		color_print_queue.popleft()

	text_commands.delete(1.0, END)
	for item in command_print_queue:
		text_commands.insert(END, item.upper() + '\n')
		text_commands.tag_add("command", "1.0", END)
		text_commands.tag_config("command", background="black", foreground="white", justify = LEFT)

	text_username.delete(1.0, END)
	for index, i in enumerate(username_print_queue):
		text_username.insert(END, username_print_queue[index] + "\n")

	for index, i in enumerate(color_print_queue):
		tag_name = "username" + str(index)
		tag_start = make_tag(index+1, 0)
		tag_end = make_tag(index+1, len(username_print_queue[index]))
		text_username.tag_add(tag_name, tag_start, tag_end)
		text_username.tag_config(tag_name, background="black", foreground=color_print_queue[index])

# count = 0
# while 1:
# 	command_printer_in = []
# 	command_printer_in.append(str(count))
# 	command_printer_in.append(['down', 'left', "up", 'right'])
# 	command_printer_in.append('white')
# 	print(command_printer_in)
# 	time.sleep(0.1)
# 	print_command_list(command_printer_in, 20, 0)
# 	user_command_root.update()
# 	count += 1