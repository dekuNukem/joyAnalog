import time
import joyanalog
import collections

replay_file = open("a.txt")
time_start = time.time()
joycon_status = collections.OrderedDict()
switch = joyanalog.joyanalog("COM5", "COM10")
switch.connect()
switch.reset()

while 1:
	this_line = replay_file.readline()[:-1]
	if(len(this_line) <= 0):
		break

	line_split = this_line.split(',')
	line_ts = float(line_split[0])
	while(time.time() - time_start < line_ts):
		continue

	joycon_status["l0"] = int(line_split[0 + 1])
	joycon_status["l1"] = int(line_split[1 + 1])
	joycon_status["lx"] = int(line_split[2 + 1])
	joycon_status["ly"] = int(line_split[3 + 1])
	joycon_status["-"] = int(line_split[4 + 1])
	joycon_status["sbl"] = int(line_split[5 + 1])
	joycon_status["cap"] = int(line_split[6 + 1])
	joycon_status["syncl"] = int(line_split[7 + 1])
	joycon_status["dd"] = int(line_split[8 + 1])
	joycon_status["du"] = int(line_split[9 + 1])
	joycon_status["dr"] = int(line_split[10 + 1])
	joycon_status["dl"] = int(line_split[11 + 1])
	joycon_status["lsr"] = int(line_split[12 + 1])
	joycon_status["lsl"] = int(line_split[13 + 1])
	joycon_status["ls"] = int(line_split[14 + 1])
	joycon_status["zl"] = int(line_split[15 + 1])

	joycon_status["r0"] = int(line_split[16 + 1])
	joycon_status["r1"] = int(line_split[17 + 1])
	joycon_status["rx"] = int(line_split[18 + 1])
	joycon_status["ry"] = int(line_split[19 + 1])
	joycon_status["+"] = int(line_split[20 + 1])
	joycon_status["sbr"] = int(line_split[21 + 1])
	joycon_status["h"] = int(line_split[22 + 1])
	joycon_status["syncr"] = int(line_split[23 + 1])
	joycon_status["y"] = int(line_split[24 + 1])
	joycon_status["x"] = int(line_split[25 + 1])
	joycon_status["b"] = int(line_split[26 + 1])
	joycon_status["a"] = int(line_split[27 + 1])
	joycon_status["rsr"] = int(line_split[28 + 1])
	joycon_status["rsl"] = int(line_split[29 + 1])
	joycon_status["rs"] = int(line_split[30 + 1])
	joycon_status["zr"] = int(line_split[31 + 1])

	switch.tas_ctrl(joycon_status)
	print(this_line)
	# time.sleep(0.005)