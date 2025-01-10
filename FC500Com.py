import serial
import time
from settings import Settings
from LoggingHandler import Logger

class FC500Com:
    def __init__(self, settings:Settings, baudrate=9600, timeout=1, max_time=1):
        self.logger = Logger()
        self.settings = settings
        self.port = self.settings.get("COMPathFC")  
        self.baudrate = baudrate
        self.timeout = timeout
        self.max_time = max_time

        self.last_response = None

        self.ser = None

        # try:
        #     self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
        # except Exception as e:
        #     self.logger.log_critical(f"An error occured while trying to create an instance of FC500 class: {e}")
        #self.ser = serial.Serial(port = "COM10", baudrate=9600, timeout=0.2)

    def connection_close(self):
        self.logger.log_info("FC500 Connection closed")
        self.ser.close()

    def connection_create(self):
        try:
            if self.ser:
                self.connection_close()
                self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
            else:
                self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
        except Exception as e:
            self.logger.log_critical(f"Exception: {e}")
            raise Exception({e})

    def connection_check(self):
        self.logger.log_info("Performing connection check on FC500 through a ping:")
        self.ping = self.cmd_ping()
        if self.ping == "MJ":
            self.logger.log_info("Ping check worked")
            return True
        else:
            self.logger.log_warning("Ping check didn't work")
            return False

    def read_data(self):
        start_time = time.time()
        self.data = "If you're reading this, something went wrong with reading data."
        self.logger.log_info(f"Waiting for data on serial port {self.port}...")
        while time.time() - start_time < self.max_time:
            if self.ser.in_waiting > 0:
                self.logger.log_info("WRITE: Read")
                self.data = self.ser.readline().decode('utf-8').rstrip()
                self.logger.log_info(self.data)
                self.last_response = self.data
                return self.data
        self.logger.log_info(f"Timed out waiting for data on serial port {self.port}...")
        return self.data

    def getLastResponse(self):
        if not self.last_response == "":
            response = self.last_response
        else:
            raise ValueError("Couldn't retrive a response.")
        return response

    def cmd_custom(self, command):
        self.logger.log_info("WRITE: A1")
        self.ser.write((command+"\r\n").encode())
        self.logger.log_info("WRITE: A2")
        self.read_data()
        return

    #Set the baseline for measurement
    def cmd_zero(self):
        command = 'ST\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Turn off FC500 (needs manual turning on) - DON'T USE
    def cmd_OFF(self):
        command = 'SS\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Put FC500 to sleep or wake it up - preferable to cmd_OFF
    def cmd_sleep(self):
        command = 'Ss\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Get a measurement
    def cmd_measure(self):
        command = 'Sx1\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Ping FC500 if it is connected
    def cmd_ping(self):
        command = 'SJ\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Set the unit of measurement
    def cmd_setunit(self):
        unit = 'N'
        command = 'Su\r\n' + unit
        self.ser.write(command.encode())
        self.read_data()
        return

    #Set how fast FC500 measures per second - needs testing
    def cmd_sethz(self):
        hz = '1000'
        command = 'St\r\n' + hz
        self.ser.write(command.encode())
        self.read_data()
        return

    #Set the gravity constant - DON'T USE
    def cmd_setgravity(self):
        gravity = 9.81
        command = 'Sn\r\n' + gravity
        self.ser.write(command.encode())
        self.read_data()
        return
    
    #Set the clock of FC500 - needs to adapted to the vaules expected by FC500
    # def cmd_setclock(self):
    #     clock = time.time
    #     command = 'Sd&t' + clock
    #     self.ser.write(command.encode())
    #     self.read_data()
    #     return
    
    #Check the clock
    def cmd_getclock(self):
        command = 'Sd&t?\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Check hz of measurement
    def cmd_gethz(self):
        command = 'St?\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return

    #Check battery level
    def cmd_getbattery(self):
        command = 'Sb\r\n'
        self.ser.write(command.encode())
        self.read_data()
        return