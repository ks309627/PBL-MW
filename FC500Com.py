import serial
import time
from settings import Settings
from LoggingHandler import Logger

class FC500Com:
    _instance = None

    def __new__(cls, settings:Settings):
        if cls._instance is None:
            cls._instance = super(FC500Com, cls).__new__(cls)
        return cls._instance

    def __init__(self, settings:Settings, baudrate=9600, timeout=0.2, max_time=2):
        if not hasattr(self, 'initialized'):
            self.logger = Logger()
            self.settings = settings
            self.port = self.settings.get("COMPathFC")
            self.baudrate = baudrate
            self.timeout = timeout
            self.max_time = max_time
            self.last_response = None
            try:
                self.ser = serial.Serial(port = self.port, baudrate = self.baudrate, timeout= self.timeout)
            except serial.SerialException as e:
                self.logger.log_warning(f"Failed to open COM port: {e}")
            self.initialized = True

    def connection_close(self):
        self.logger.log_info("FC500 Connection closed")
        self.ser.close()

    def connection_create(self):
        try:
            if self.ser:
                self.connection_close()
                self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
                self.logger.log_info("FC500 Connection opened")
            else:
                self.ser = serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout)
        except Exception:
            raise

    def connection_check(self):
        self.logger.log_info("Performing connection check on FC500 through a ping:")
        self.ping = self.cmd_ping()
        self.logger.log_info(self.ping)
        if self.ping == "MJ":
            self.logger.log_info("Ping check worked")
            return True
        else:
            self.logger.log_warning("Ping check didn't work")
            return False

    def read_data(self, silent):
        start_time = time.time()
        self.data = "If you're reading this, something went wrong with reading data."
        if silent == False:
            self.logger.log_info(f"Waiting for data on serial port {self.port}...")
        while time.time() - start_time < self.max_time:
            if self.ser.in_waiting > 0:
                self.data = self.ser.readline().decode('utf-8').rstrip()
                if silent == False:
                    self.logger.log_info(self.data)
                self.last_response = self.data
                return self.data
        self.logger.log_info(f"Timed out waiting for data on serial port {self.port}...")
        return

    def getLastResponse(self):
        if not self.last_response == "":
            response = self.last_response
        else:
            raise ValueError("Couldn't retrive a response.")
        return response

    def cmd_custom(self, command, silent=False):
        try:
            self.ser.write((command+"\r\n").encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Set the baseline for measurement
    def cmd_zero(self, silent=False):
        command = 'ST\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Turn off FC500 (needs manual turning on) - DON'T USE
    def cmd_OFF(self, silent=False):
        command = 'SS\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Put FC500 to sleep or wake it up - preferable to cmd_OFF
    def cmd_sleep(self, silent=False):
        command = 'Ss\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Get a measurement
    def cmd_measure(self, silent=False):
        command = 'Sx1\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Ping FC500 if it is connected
    def cmd_ping(self, silent=False):
        command = 'SJ\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        data = self.read_data(silent)
        return data

    #Set the unit of measurement
    def cmd_setunit(self, silent=False):
        unit = 'N'
        command = 'Su\r\n' + unit
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Set how fast FC500 measures per second - needs testing
    def cmd_sethz(self, silent=False):
        hz = '1000'
        command = 'St\r\n' + hz
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Set the gravity constant - DON'T USE
    def cmd_setgravity(self, silent=False):
        gravity = 9.81
        command = 'Sn\r\n' + gravity
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return
    
    #Set the clock of FC500 - needs to adapted to the vaules expected by FC500
    # def cmd_setclock(self, silent=False):
    #     clock = time.time
    #     command = 'Sd&t' + clock
    #     try:
    #         self.ser.write(command.encode())
    #     except Exception as e:
    #         self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
    #         return
    #     self.read_data(silent)
    #     return
    
    #Check the clock
    def cmd_getclock(self, silent=False):
        command = 'Sd&t?\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Check hz of measurement
    def cmd_gethz(self, silent=False):
        command = 'St?\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return

    #Check battery level
    def cmd_getbattery(self, silent=False):
        command = 'Sb\r\n'
        try:
            self.ser.write(command.encode())
        except Exception as e:
            self.logger.log_error(f"{e}. Probable cause: Connection closed before receiving a response.")
            return
        self.read_data(silent)
        return