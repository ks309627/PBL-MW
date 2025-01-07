import serial
import time
from settings import Settings
from LoggingHandler import Logger

class FC500Com:
    def __init__(self, settings:Settings, baudrate=9600, timeout=0.2, max_time=0.5):
        self.logger = Logger()
        self.settings = settings
        self.port = self.settings.get("COMPathFC")  
        self.baudrate = baudrate
        self.timeout = timeout
        self.max_time = max_time
        #self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
        #self.ser = serial.Serial(port = "COM10", baudrate=9600, timeout=0.2)

    def connection_check(self):
        start_time = time.time()
        while time.time() - start_time < self.max_time:
            if self.ser.in_waiting > 0:
                return True
        return False

    def read_data(self):
        self.ser.flush()
        data = "If you're seing this, something went wrong with Read Data."
        while self.connection_check():
            data = self.ser.readline().decode('utf-8').rstrip()
            self.logger.log_info(data)
        return data

    def close(self):
        self.ser.close()

    def cmd_custom(self, command):
        self.ser.write((command+"\r\n").encode())
        response = self.read_data()
        return response

    #Set the baseline for measurement
    def cmd_zero(self):
        command = 'ST\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Turn off FC500 (needs manual turning on) - DON'T USE
    def cmd_OFF(self):
        command = 'SS\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Put FC500 to sleep or wake it up - preferable to cmd_OFF
    def cmd_sleep(self):
        command = 'Ss\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        self.logger.log_info(response)
        return response

    #Get a measurement
    def cmd_measure(self):
        command = 'Sx1\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Ping FC500 if it is connected
    def cmd_ping(self):
        command = 'SJ\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set the unit of measurement
    def cmd_setunit(self):
        unit = 'N'
        command = 'Su\r\n' + unit
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set how fast FC500 measures per second - needs testing
    def cmd_sethz(self):
        hz = '1000'
        command = 'St\r\n' + hz
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Set the gravity constant - DON'T USE
    def cmd_setgravity(self):
        gravity = 9.81
        command = 'Sn\r\n' + gravity
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
        command = 'Sd&t?\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Check hz of measurement
    def cmd_gethz(self):
        command = 'St?\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response

    #Check battery level
    def cmd_getbattery(self):
        command = 'Sb\r\n'
        self.ser.write(command.encode())
        response = self.read_data()
        return response