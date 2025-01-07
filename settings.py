import os
from LoggingHandler import Logger

class Settings:
    def __init__(self, config_file="config.txt"):
        self.logger = Logger()
        self.config_file = os.path.abspath(config_file)
        self.default_settings = {
            "devMode": 0,
            "graphSavePath": os.getcwd(), # v03.01.25.1
            "COMPathFC": "COM1",
            "COMPathESP": "COM2"
        }
        self.settings = self.default_settings.copy()
        self.load_settings()

    def save_settings(self):
        with open(self.config_file, 'w') as file:
            for key, value in self.settings.items():
                file.write(f"{key} = {value}\n")
        self.logger.log_info(f"Ustawienia zapisane do pliku: {self.config_file}")

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                for line in file:
                    key, value = line.strip().split(' = ', 1)
                    self.settings[key] = int(value) if value.isdigit() else value
            self.logger.log_info("Ustawienia wczytane.")
        else:
            self.logger.log_info("Utworzono plik ustawień z wartościami domyślnymi.")
            self.save_settings()


    def reset_to_defaults(self):
        self.settings = self.default_settings.copy()
        self.save_settings()
        self.logger.log_info("Ustawienia zostały przywrócone do wartości domyślnych.")

    def get(self, key):
        return self.settings.get(key, None)

    def set(self, key, value):
        self.settings[key] = value

    def get_graph_save_path(self):
        path = self.get("graphSavePath")
        if not os.path.exists(path):
            self.logger.log_error(f"Ścieżka {path} nie istnieje. Używana będzie domyślna ścieżka: {self.default_settings['graphSavePath']}")
            return self.default_settings["graphSavePath"]
        return path