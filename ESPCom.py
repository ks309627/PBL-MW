import serial
import time
from settings import Settings
from LoggingHandler import Logger

class ESPCom:
    
    _instance = None

    def __new__(cls, settings: Settings, baudrate=9600, timeout=1):
        if cls._instance is None:
            cls._instance = super(ESPCom, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, settings: Settings, baudrate=9600, timeout=1):
        if not hasattr(self, 'initialized'):
            self.logger = Logger()
            self.settings = settings
            self.port = self.settings.get("COMPathESP")
            self.baudrate = baudrate
            self.timeout = timeout
            self.serial_connection = None

            try:
                self.serial_connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                self.logger.log_info(f"Połączono z ESP na porcie {self.port}")
            except serial.SerialException as e:
                self.logger.log_warning(f"Nie udało się otworzyć portu COM: {e}")

            self.initialized = True  # Flaga inicjalizacji




    def connect(self):
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()

            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Daje czas ESP na inicjalizację
            self.logger.log_info(f"Połączono z {self.port} przy {self.baudrate} bps")
            self.initialized = True

            # Sprawdzenie, czy ESP odpowiada
            self.serial_connection.write(b"test\n")
            response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
            if response:
                self.logger.log_info(f"ESP odpowiedział: {response}")
                return True, f"Connected to {self.port} at {self.baudrate} bps"
            else:
                self.logger.log_warning("Brak odpowiedzi od ESP")
                return False, "ESP nie odpowiada"

        except serial.SerialException as e:
            self.logger.log_warning(f"Nie udało się otworzyć portu COM: {e}")
            return False, str(e)

    def cmd_custom(self, command, silent=False):
        if not self.initialized or not self.serial_connection or not self.serial_connection.is_open:
            self.logger.log_error("ESP nie jest połączone")
            return None

        full_command = f"{command}\n"
        self.serial_connection.write(full_command.encode('utf-8'))
        self.logger.log_info(f"Wysłano: {full_command.strip()}")
        
        response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
        if response:
            print(f"Odpowiedź ESP: {response}")
            return response
        return None

    def connection_close(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.logger.log_info("Połączenie z ESP zamknięte")