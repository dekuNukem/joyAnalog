import time
import serial

JOYCON_BUTTONS_LEFT = ["du", "dd", "dl", "dr", "ls", "zl", "-", "cap", "lsl", "lsr", "syncl", "sbl"]
JOYCON_BUTTONS_RIGHT = ["a", "b", "x", "y", "rs", "zr", "+", "h", "rsl", "rsr", "syncr", "sbr"]

class switch_ctrl:
    def __init__(self, serial_port1, serial_port2):
        self.port1 = serial_port1
        self.port2 = serial_port2
        self.ser1 = serial.Serial()
        self.ser2 = serial.Serial()
        self.ser_left = serial.Serial()
        self.ser_right = serial.Serial()

    def connect(self):
        while 1:
            try:
                time.sleep(1.2)
                self.ser1.close()
                self.ser2.close()
                self.ser1 = serial.Serial(self.port1, 115200)
                print(self.port1 + " opened successfully")
                self.ser2 = serial.Serial(self.port2, 115200)
                print(self.port2 + " opened successfully")
                self.ser1.write("whoami\n".encode('utf-8'))
                ser1_result = self.ser1.readline().decode('utf-8')
                self.ser2.write("whoami\n".encode('utf-8'))
                ser2_result = self.ser2.readline().decode('utf-8')
                break
            except Exception as e:
                print("exception trying to connect: " + str(e))
                continue

        if ser1_result == ser2_result:
            print("ERROR: both boards are same side")
            exit()
        elif "LEFT" not in ser1_result and "RIGHT" not in ser1_result:
            print("ERROR: unknown board type on " + self.port1)
            exit()
        elif "LEFT" not in ser2_result and "RIGHT" not in ser2_result:
            print("ERROR: unknown board type on " + self.port2)
            exit()

        if "LEFT" in ser1_result:
            self.ser_left = self.ser1
            self.ser_right = self.ser2
        else:
            self.ser_left = self.ser2
            self.ser_right = self.ser1
        print("left joycon is: " + str(self.ser_left.port))
        print("right joycon is: " + str(self.ser_right.port))
        print("ports open successful")

    def disconnect(self):
        print("disconnecting...")
        self.reset()
        self.ser1.close()
        self.ser2.close()

    def send(self, ser_port, message):
        if len(message) <= 0:
            return
        try:
            ser_port.write(message.encode('utf-8'))
        except Exception as e:
            print("serial write error:\nport: " + str(ser_port.port) + "\nexception: " + str(e))
            self.connect()
        print(str(ser_port.port) + " sent: " + message)

    def recvln(self, ser_port):
        result = ''
        try:
            result = ser_port.readline().decode('utf-8')
        except Exception as e:
            print("serial read error:\nport: " + str(ser_port.port) + "\nexception: " + str(e))
            self.connect()
        print(str(ser_port.port) + " received: " + result)
        return result

    def check_error(self, left_message, right_message, left_result, right_result):
        if "ERROR" in left_result:
            raise ValueError('LEFT joycon\nsent: ' + str(left_message) + '\nreceived: ' + left_result + '\n')
        if "ERROR" in right_result:
            raise ValueError('RIGHT joycon\nsent: ' + str(right_message) + '\nreceived: ' + right_result + '\n')

    def button_click(self, duration_ms, button_list):
        left_message = ''
        right_message = ''
        left_result = ''
        right_result = ''
        left_queue = [x for x in button_list if x in JOYCON_BUTTONS_LEFT][:16]
        right_queue = [x for x in button_list if x in JOYCON_BUTTONS_RIGHT][:16]
        if len(left_queue) > 0:
            left_message = "bc " + str(duration_ms) + " "
            for item in left_queue:
                left_message += item + " "
            left_message += '\n'
        if len(right_queue) > 0:
            right_message = "bc " + str(duration_ms) + " "
            for item in right_queue:
                right_message += item + " "
            right_message += '\n'
        self.send(self.ser_left, left_message)
        self.send(self.ser_right, right_message)
        if len(left_message) > 0:
            left_result = self.recvln(self.ser_left)
        if len(right_message) > 0:
            right_result = self.recvln(self.ser_right)
        self.check_error(left_message, right_message, left_result, right_result)

    def button_hold(self, button_list):
        left_message = ''
        right_message = ''
        left_result = ''
        right_result = ''
        left_queue = [x for x in button_list if x in JOYCON_BUTTONS_LEFT][:16]
        right_queue = [x for x in button_list if x in JOYCON_BUTTONS_RIGHT][:16]
        if len(left_queue) > 0:
            left_message = "bh "
            for item in left_queue:
                left_message += item + " "
            left_message += '\n'
        if len(right_queue) > 0:
            right_message = "bh "
            for item in right_queue:
                right_message += item + " "
            right_message += '\n'
        self.send(self.ser_left, left_message)
        self.send(self.ser_right, right_message)
        if len(left_message) > 0:
            left_result = self.recvln(self.ser_left)
        if len(right_message) > 0:
            right_result = self.recvln(self.ser_right)
        self.check_error(left_message, right_message, left_result, right_result)

    def button_release(self, button_list):
        left_message = ''
        right_message = ''
        left_result = ''
        right_result = ''
        left_queue = [x for x in button_list if x in JOYCON_BUTTONS_LEFT][:16]
        right_queue = [x for x in button_list if x in JOYCON_BUTTONS_RIGHT][:16]
        if len(left_queue) > 0:
            left_message = "br "
            for item in left_queue:
                left_message += item + " "
            left_message += '\n'
        if len(right_queue) > 0:
            right_message = "br "
            for item in right_queue:
                right_message += item + " "
            right_message += '\n'
        self.send(self.ser_left, left_message)
        self.send(self.ser_right, right_message)
        if len(left_message) > 0:
            left_result = self.recvln(self.ser_left)
        if len(right_message) > 0:
            right_result = self.recvln(self.ser_right)
        self.check_error(left_message, right_message, left_result, right_result)

    def button_release_all(self):
        message = 'bra\n'
        self.send(self.ser_left, message)
        self.send(self.ser_right, message)
        left_result = self.recvln(self.ser_left)
        right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)

    def stick_hold(self, side, x, y):
        left_result = ''
        right_result = ''
        message = "sh " + str(x) + " " + str(y) + "\n"
        if side.lower().startswith("l"):
            self.send(self.ser_left, message)
        elif side.lower().startswith("r"):
            self.send(self.ser_right, message)
        else:
            return
        if side.lower().startswith("l"):
            left_result = self.recvln(self.ser_left)
        elif side.lower().startswith("r"):
            right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)

    def stick_hold_dual(self, x_left, y_left, x_right, y_right):
        left_message = "sh " + str(x_left) + " " + str(y_left) + "\n"
        right_message = "sh " + str(x_right) + " " + str(y_right) + "\n"
        self.send(self.ser_left, left_message)
        self.send(self.ser_right, right_message)
        left_result = self.recvln(self.ser_left)
        right_result = self.recvln(self.ser_right)
        self.check_error(left_message, right_message, left_result, right_result)

    def stick_release(self, side):
        left_result = ''
        right_result = ''
        message = "sr\n"
        if side.lower().startswith("l"):
            self.send(self.ser_left, message)
        elif side.lower().startswith("r"):
            self.send(self.ser_right, message)
        else:
            return
        if side.lower().startswith("l"):
            left_result = self.recvln(self.ser_left)
        elif side.lower().startswith("r"):
            right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)

    def stick_release_dual(self):
        self.stick_release("l")
        self.stick_release("r")

    def stick_disengage(self, side):
        left_result = ''
        right_result = ''
        message = "sd\n"
        if side.lower().startswith("l"):
            self.send(self.ser_left, message)
        elif side.lower().startswith("r"):
            self.send(self.ser_right, message)
        else:
            return
        if side.lower().startswith("l"):
            left_result = self.recvln(self.ser_left)
        elif side.lower().startswith("r"):
            right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)

    def stick_disengage_dual(self):
        self.stick_disengage("l")
        self.stick_disengage("r")

    def stick_nudge(self, side, duration_ms, x, y):
        left_result = ''
        right_result = ''
        message = "sn " + str(duration_ms) + " " + str(x) + " " + str(y) + "\n"
        if side.lower().startswith("l"):
            self.send(self.ser_left, message)
        elif side.lower().startswith("r"):
            self.send(self.ser_right, message)
        else:
            return
        if side.lower().startswith("l"):
            left_result = self.recvln(self.ser_left)
        elif side.lower().startswith("r"):
            right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)

    def reset(self):
        message = "reset\n"
        self.send(self.ser_left, message)
        self.send(self.ser_right, message)
        left_result = self.recvln(self.ser_left)
        right_result = self.recvln(self.ser_right)
        self.check_error(message, message, left_result, right_result)
