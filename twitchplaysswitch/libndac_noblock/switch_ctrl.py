import time
import copy
import serial

class switch_ctrl:
    def __init__(self, serial_port):
        self.board_type = ''
        self.port = serial_port
        self.ser = serial.Serial()
        self.rx_buf = ''

    def connect(self):
        try:
            self.ser.close()
        except Exception as e:
            print("exception trying to close: " + str(e))
        while 1:
            try:
                self.rx_buf = ''
                time.sleep(1.2)
                self.ser = serial.Serial(self.port, 115200)
                print("port opened successfully")
                self.send("whoami\n")
                self.board_type = self.readline_blocking()
                if "LEFT" not in self.board_type and "RIGHT" not in self.board_type:
                    print("unkown board type: " + self.board_type)
                    exit()
                self.reset()
                return
            except Exception as e:
                print("exception trying to connect: " + str(e))

    def readline_noblock(self):
        if self.ser.inWaiting() > 0:
            self.rx_buf += self.ser.read(self.ser.inWaiting()).decode('utf-8')
        if len(self.rx_buf) > 0 and self.rx_buf[-1] == '\n':
            ret = copy.deepcopy(self.rx_buf)
            self.rx_buf = ''
            print("got: " + str(ret))
            return ret
        return ""

    def readline_blocking(self):
        while 1:
            ret = self.readline_noblock()
            if ret != '':
                return ret

    def cmd_available(self):
        result = self.readline_noblock()
        if result == '':
            return False
        if "ok" in result.lower():
            return True
        if "ERROR" in result or "?" in result:
            raise ValueError('invalid response: ' + result + '\n') 
        return False

    def send(self, message):
        try:
            print("sending: " + message)
            self.ser.write(message.encode('utf-8'))
        except Exception as e:
            print("serial write exception: " + str(e))
            self.connect()

    def button_hold(self, buttons):
        message = "bh " + str(buttons).lower() + "\n"
        self.send(message)

    def button_release(self, buttons):
        message = "br " + str(buttons).lower() + "\n"
        self.send(message)

    def button_release_all(self):
        self.send("bra\n")

    def button_click(self, duration_ms, buttons):
        message = "bc " + str(duration_ms) + " " + str(buttons).lower() + "\n"
        self.send(message)

    def stick_hold(self, x, y):
        message = "sh " + str(x) + " " + str(y) + "\n"
        self.send(message)

    def stick_release(self):
        self.send("sr\n")

    def stick_nudge(self, duration_ms, x, y):
        message = "sn " + str(duration_ms) + " " + str(x) + " " + str(y) + "\n"
        self.send(message)

    def stick_disengage(self):
        self.send("sd\n")

    def reset(self):
        self.send("reset\n")