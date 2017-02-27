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
                time.sleep(1.5)
                self.ser = serial.Serial(self.port, 115200)
                print("port opened successfully")
                self.send("whoami\n")
                self.board_type = self.readline_blocking()
                if "LEFT" not in self.board_type and "RIGHT" not in self.board_type:
                    print("unkown board type: " + self.board_type)
                    exit()
                self.release_all()
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
            raise ValueError('invalid command/argument\nsent: ' + str(message) + '\nreceived: ' + result + '\n') 
        return False

    def send(self, message):
        try:
            self.ser.write(message.encode('utf-8'))
        except Exception as e:
            print("serial write exception: " + str(e))
            self.connect()

    def sleep_ms(self, delay_ms):
        time.sleep(float(delay_ms)/1000)

    def button_hold(self, buttons):
        message = "bh " + str(buttons).lower() + "\n"
        self.send(message)

    def button_release(self, buttons):
        message = "br " + str(buttons).lower() + "\n"
        self.send(message)

    def button_click(self, buttons, duration_ms):
        self.button_hold(buttons)
        self.sleep_ms(duration_ms)
        self.button_release(buttons)
        self.sleep_ms(duration_ms)

    def button_release_all(self):
        self.send("bra\n")

    def stick_hold(self, x, y):
        message = "sh " + str(x) + " " + str(y) + "\n"
        self.send(message)

    def stick_nudge(self, x, y, duration_ms):
        self.stick_hold(x, y)
        self.sleep_ms(duration_ms)
        self.stick_release()
        self.sleep_ms(duration_ms)

    def stick_release(self):
        self.send("sr\n")

    def stick_disengage(self):
        self.send("sd\n")

    def release_all(self):
        self.button_release_all()
        self.stick_release()