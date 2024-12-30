import serial
import time

class FC500Com:
    def __init__(self, port= '/dev/ttyUSB0', baudrate=9600, timeout=0.2, max_time=0.5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.max_time = max_time
        self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)

    def connection_check(self):
        start_time = time.time()
        while time.time() - start_time < self.max_time:
            if self.ser.in_waiting > 0:
                return True
        return False


    def read_data(self):
        self.ser.flush()
        data = ''
        while True:
            if self.connection_check():
                data = self.ser.readline().decode('utf-8').rstrip()
                print(f"Received data: {data}")
            else:
                break
        return 1

    def close(self):
        self.ser.close()

    #Set the baseline for measurement
    def cmd_zero(self):
        command = 'ST'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Turn off FC500 (needs manual turning on) - DON'T USE
    def cmd_OFF(self):
        command = 'SS'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Put FC500 to sleep or wake it up - preferable to cmd_OFF
    def cmd_sleep(self):
        command = 'Ss'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Get a measurement
    def cmd_measure(self):
        command = 'Sx1'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Ping FC500 if it is connected
    def cmd_ping(self):
        command = 'SJ'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set the unit of measurement
    def cmd_setunit(self):
        unit = 'N'
        command = 'Su' + unit
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set how fast FC500 measures per second - needs testing
    def cmd_sethz(self):
        hz = '1000'
        command = 'St' + hz
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set the gravity constant - DON'T USE
    def cmd_setgravity(self):
        gravity = 9.81
        command = 'Sn' + gravity
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set the clock of FC500 - needs to adapted to the vaules expected by FC500
    # def cmd_setclock(self):
    #     clock = time.time
    #     command = 'Sd&t' + clock
    #     self.ser.write(command.encode())
    #     response = self.read_data()
    #     return response
    
    #Check the clock
    def cmd_getclock(self):
        command = 'Sd&t?'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Check hz of measurement
    def cmd_gethz(self):
        command = 'St?'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Check battery level
    def cmd_getbattery(self):
        command = 'Sb'
        self.ser.write(command.encode())
        response = self.read_data()
        return response