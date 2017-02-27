import os
import sys
import time
import socket
from datetime import datetime

class tmi_message(object):
	def __init__(self):
		self.color = None
		self.display_name = None
		self.emotes = None
		self.is_subscriber = None
		self.is_turbo = None
		self.user_type = None
		self.username = None
		self.message = None
		self.timestamp = None
		self.raw_message = None
		self.message_type = None
		self.emote_sets = None
		self.msg_id = None
		self.channel = None

def iso8601_utc_now():
	return datetime.utcnow().isoformat(sep='T') + "Z"

def log_error(content):
	with open("err_log.txt", 'a') as err_log:
		err_log.write(iso8601_utc_now() + " " + str(content) + '\n')

def parse_tags(raw_tag):
	ret = {'color':None, 'display-name':None, 'emotes':None, 'subscriber':0, 'turbo':0, 'user-type':None, 'emote-sets':None, 'msg-id':None}
	try:
		if len(raw_tag) > 0:
			for item in raw_tag.split(';'):
				split_tag = item.split('=')
				ret[split_tag[0]] = split_tag[1]
	except Exception as e:
		err_msg = "Exception at parse_tags: " + str(e) + ", raw_tag: " + str(raw_tag)
		print(err_msg)
		log_error(err_msg)
	return ret

def parse_msg(raw_msg):
	msg_type = ''
	sender = ''
	channel = ''
	message = ''
	try:
		msg_split = raw_msg.split(' ', 3)
		sender = msg_split[0].lstrip(':').split('!')[0]
		msg_type = msg_split[1]
		channel = msg_split[2]
		message = ''
		if len(msg_split) >= 4:
			message = msg_split[3][1:]
	except Exception as e:
		err_msg = "Exception at parse_msg: " + str(e) + ", raw_msg: " + str(raw_msg)
		print(err_msg)
		log_error(err_msg)
	return msg_type, sender, channel, message

def parse_raw(raw):
	ret = tmi_message()
	ret.raw_message = raw
	ret.timestamp = time.time()
	raw_msg = raw
	if raw.startswith("@"):
		split = raw.lstrip("@").split(' ', 1)
		raw_msg = split[1]
		tag_dict = parse_tags(split[0])
		ret.color = tag_dict['color']
		ret.display_name = tag_dict['display-name']
		ret.emotes = tag_dict['emotes']
		ret.is_subscriber = bool(int(tag_dict['subscriber']))
		ret.is_turbo = bool(int(tag_dict['turbo']))
		ret.user_type = tag_dict['user-type']
		ret.emote_sets = tag_dict['emote-sets']
	msg_type, sender, msg_channel, comment = parse_msg(raw_msg)
	ret.message_type = msg_type
	ret.username = sender
	ret.channel = msg_channel
	ret.message = comment
	return ret

class irc_bot(object):
	def __init__(self, nickname, oauth, channel, host, port, timeout = 600, membership = 0, commands = 0, tags = 0):
		self.NICK = nickname
		self.AUTH = oauth
		self.CHAT_CHANNEL = channel
		self.HOST = host
		self.PORT = int(port)
		self.sock = socket.socket()
		self.timeout = timeout
		self.request_membership = membership
		self.request_commands = commands
		self.request_tags = tags
		self.is_connected = False
		self.last_message = ''
		self.recv_buffer = ''

	def connect(self):
		del self.sock
		self.sock = socket.socket()
		self.sock.settimeout(self.timeout)
		self.sock.connect((self.HOST, self.PORT))
		self.sock.send(bytes("PASS %s\r\n" % self.AUTH, "UTF-8"))
		self.sock.send(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
		self.sock.send(bytes("USER %s %s bla :%s\r\n" % (self.NICK, self.HOST, self.NICK), "UTF-8"))
		self.sock.send(bytes("JOIN #%s\r\n" % self.CHAT_CHANNEL, "UTF-8"));
		print(self.NICK + ": connected to " + self.CHAT_CHANNEL)
		if self.request_membership:
			self.sock.send(bytes("CAP REQ :twitch.tv/membership\r\n", "UTF-8"))
		if self.request_commands:
			self.sock.send(bytes("CAP REQ :twitch.tv/commands\r\n", "UTF-8"))
		if self.request_tags:
			self.sock.send(bytes("CAP REQ :twitch.tv/tags\r\n", "UTF-8"))
		self.is_connected = True
		self.sock.setblocking(0)

	def update(self):
		if not self.is_connected:
			self.retry_connect()	
		ret = []
		self.recv_buffer += self.sock.recv(1024).decode("UTF-8", errors = "ignore")
		raw_msg_list = self.recv_buffer.split("\r\n")
		self.recv_buffer = raw_msg_list[-1]
		for item in raw_msg_list[:-1]:
			if "PRIVMSG" not in item and "tmi.twitch.tv RECONNECT" in item:
				err_msg = self.NICK + ": server requested RECONNECT"
				print(err_msg)
				log_error(err_msg)
				self.retry_connect()
				break
			if "PRIVMSG" not in item and 'tmi.twitch.tv' in item and 'PING' in item:
				self.sock.send(bytes("PONG tmi.twitch.tv\r\n", "UTF-8"))
			if "PRIVMSG" not in item and "tmi.twitch.tv" in item and ("Login unsuccessful" in item or "Error logging in" in item):
				print(self.NICK + ": Login failed! check your username and oauth")
				retry_connect()
				break
			ret.insert(0, item)
		return ret
			
	def retry_connect(self):
		while 1:
			time.sleep(1)
			try:
				self.connect()
			except Exception as e:
				print("Exception while trying to connect: " + str(type(e)) + ": " + str(e))
				time.sleep(1)
				continue
			return

	def get_raw_message(self):
		try:
			return self.update()
		except Exception as e:
			return []

	def get_parsed_message(self):
		ret = []
		for item in self.get_raw_message():
			if item == "PING :tmi.twitch.tv":
				continue
			ret.append(parse_raw(item))
		return ret

	def send_message(self, message):
		if message == self.last_message:
			message = message + " "
		try:
			self.sock.send(bytes("PRIVMSG #%s :%s\r\n" % (self.CHAT_CHANNEL, message), "UTF-8"))
			self.last_message = message
		except Exception as e:
			print("Exception sending message: " + str(type(e)) + ": " + str(e))
			self.retry_connect()