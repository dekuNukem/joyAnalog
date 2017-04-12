# https://pypi.python.org/pypi/inputs

from inputs import devices, get_gamepad

for device in devices:
	try:
		print(device)
	except Exception as e:
		print(e)

while 1:
	events = get_gamepad()
	for event in events:
		print(event.ev_type, event.code, event.state)