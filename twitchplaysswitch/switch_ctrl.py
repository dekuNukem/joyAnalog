import time
import serial

class switch_ctrl:
    def __init__(self, serial_port):
        self.board_type = ''
        self.port = serial_port
        self.ser = serial.Serial()

    def connect(self):
        try:
            self.ser.close()
        except Exception as e:
            print("exception trying to close: " + str(e))
        while 1:
            try:
                time.sleep(1.5)
                self.ser = serial.Serial(self.port, 115200)
                print("port opened successfully")
                self.board_type = self.send("whoami\n")
                if "LEFT" not in self.board_type and "RIGHT" not in self.board_type:
                    print("unkown board type: " + self.board_type)
                    exit()
                return
            except Exception as e:
                print("exception trying to connect: " + str(e))

    def send(self, message):
        result = ''
        try:
            self.ser.write(message.encode('utf-8'))
            result = self.ser.readline().decode('utf-8')
        except Exception as e:
            print("serial write exception: " + str(e))
            self.connect()
        print(result)
        if "ERROR" in result or "?" in result:
            raise ValueError('invalid command/argument\nsent: ' + str(message) + '\nreceived: ' + result + '\n')
        return result

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