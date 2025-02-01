import serial
import time
from settings import Settings
from LoggingHandler import Logger

class ESPCom: #changed SerialCommunicator to ESPCom
    def __init__(self, settings: Settings, baudrate=9600, timeout=1):
        self.logger = Logger()
        self.settings = settings
        self.port = self.settings.get("COMPathESP")
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        try:
            self.ser = serial.Serial(port = self.port, baudrate = self.baudrate, timeout= self.timeout)
        except serial.SerialException as e:
            self.logger.log_warning(f"Failed to open COM port: {e}")
        self.initialized = True
    
    def cmd_custom(self, command, silent=False):
        full_command = f"{command}\r\n"
        self.ser.write(full_command.encode('utf-8'))
        self.logger.log_info(f"ESP - Wysłano komendę: {full_command.strip()}")
        response = self.ser.readline().decode('utf-8', errors='ignore').strip()
        if response:
            print(f"ESP - Otrzymano wiadomość: {response}")
            return response
    
    def connection_close(self):
        self.logger.log_info("ESP Connection closed")
        self.ser.close()

    def update_com_path(self, new_port):
        self.port = new_port
        self.logger.log_info(f"[INFO]: Port COM zaktualizowany na {self.port}")
    
    #nw czy to będzie działać
    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            return True, f"Connected to {self.port} at {self.baud_rate} bps"
        except Exception as e:
            return False, f"Error: {e}"

