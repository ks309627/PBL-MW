import json
import os
import time

class ForceChecker:
    def __init__(self):
        self.default_limit = 20
        self.directory = 'graphs/'
        self.file_extension = '.json'

    def get_most_recent_file(self):
        files = [self.directory + f for f in os.listdir(self.directory) if f.endswith(self.file_extension)]
        if not files:
            raise FileNotFoundError("No JSON files found in the directory")
        return max(files, key=os.path.getctime)

    def force_check(self, limit=None):
        """Sprawdza, czy w przeciągu ostatnich `limit` sekund wartość force się zmieniła."""
        if limit is None:
            limit = self.default_limit
        recent_file = self.get_most_recent_file()

        with open(recent_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Sprawdzenie, czy klucze istnieją
        if "force" not in data or "seconds" not in data:
            raise KeyError("Brak klucza 'force' lub 'seconds' w danych JSON.")

        # Konwersja wartości force na float, usunięcie jednostki 'N'
        force_values = [float(value.replace(" ", "").replace("N", "")) for value in data["force"]]
        time_values = data["seconds"]

        # Sprawdzenie poprawności danych
        if len(force_values) != len(time_values):
            raise ValueError("Nieprawidłowa długość list w danych JSON.")

        # Pobranie aktualnego czasu (ostatnia wartość w pliku JSON)
        current_time = time_values[-1]
        latest_force = force_values[-1]  # Ostatnia wartość siły

        # Przeszukanie danych od teraz do `limit` sekund wstecz
        for i in range(len(time_values) - 1, -1, -1):
            if current_time - time_values[i] > limit:
                break  # Jeśli czas przekroczył `limit`, kończymy pętlę

            if force_values[i] != latest_force:
                return True  # Znaleziono zmianę wartości w danym zakresie

        return False  # Brak zmian wartości force w podanym czasie
