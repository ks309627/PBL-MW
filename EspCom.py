# v30.11.24.2
import serial
from settings import Settings

class SerialCommunicator:
    def __init__(self, settings:Settings, baud_rate=9600):
        self.settings = settings
        self.port = self.settings.get("COMPathESP")  
        self.baud_rate = baud_rate
        self.serial_connection = None

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            return True, f"Connected to {self.port} at {self.baud_rate} bps"
        except Exception as e:
            return False, f"Error: {e}"

    def update_com_path(self, new_port):
        """Aktualizuje port COM."""
        self.port = new_port
        print(f"[INFO]: Port COM zaktualizowany na {self.port}")

    def send_command(self, command):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                self.serial_connection.write(command.encode())
                response = self.serial_connection.read_all().decode().strip()
                return f"Sent: {command}\nResponse: {response}"
            except Exception as e:
                return f"Error: {e}"
        else:
            return "Serial connection is not open"

    def send_left_command(self):
        return self.send_command("left")

    def send_right_command(self):
        return self.send_command("right")

    def close(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            return "Connection closed"
        return "Connection already closed"
