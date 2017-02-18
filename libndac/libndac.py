import time
import serial

ser = serial.Serial('COM5')

while 1:
	ser.write(b'bh a\n')
	ser.readline()

	ser.write(b'br a\n')
	ser.readline()
