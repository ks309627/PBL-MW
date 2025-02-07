import json
import os
import time

class ForceChecker:
    def __init__(self):
        self.default_limit = 20
        self.directory = 'graphs/'
        self.file_extension = '.json'

    def get_most_recent_file(self):
        """Znajduje najnowszy folder w 'graphs/' i wyszukuje w nim plik JSON o tej samej nazwie."""
        
        # Pobranie listy wszystkich folderów w 'graphs/' posortowanych po dacie utworzenia
        folders = [f for f in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, f))]
        if not folders:
            raise FileNotFoundError("Brak folderów w katalogu 'graphs/'")

        # Znalezienie najnowszego folderu
        latest_folder = max(folders, key=lambda f: os.path.getctime(os.path.join(self.directory, f)))
        folder_path = os.path.join(self.directory, latest_folder)

        # Sprawdzenie, czy w folderze znajduje się plik JSON o tej samej nazwie co folder
        json_file_path = os.path.join(folder_path, f"{latest_folder}.json")
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku {latest_folder}.json w folderze {folder_path}")

        return json_file_path  # Zwraca pełną ścieżkę do pliku JSON

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
