import os

class Settings:
    def __init__(self, config_file="config.txt"):
        self.config_file = os.path.abspath(config_file)
        self.default_settings = {
            "devMode": 0,
            "graphSavePath": "test",
            "COMPath": "COM1",
            "COMPathESP": "COM2"
        }
        self.settings = self.default_settings.copy()
        self.load_settings()

    def save_settings(self):
        with open(self.config_file, 'w') as file:
            for key, value in self.settings.items():
                file.write(f"{key} = {value}\n")
        print(f"Ustawienia zapisane do pliku: {self.config_file}")

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as file:
                for line in file:
                    key, value = line.strip().split(' = ', 1)
                    self.settings[key] = int(value) if value.isdigit() else value
            print("Ustawienia wczytane.")
        else:
            self.save_settings()
            print("Utworzono plik ustawień z wartościami domyślnymi.")

    def reset_to_defaults(self):
        self.settings = self.default_settings.copy()
        self.save_settings()
        print("Ustawienia zostały przywrócone do wartości domyślnych.")

    def get(self, key):
        return self.settings.get(key, None)

    def set(self, key, value):
        self.settings[key] = value