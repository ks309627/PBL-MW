import json
import os
import time

class ForceChecker:
    def __init__(self):
        self.default_limit = 20
        self.directory = 'graphs/'
        self.file_extension = '.json'
        self.limiter_enabled = True  # ? Zmienna steruj?ca dzia?aniem limitera

    def toggle_limiter(self, enabled):
        """W??cza lub wy??cza limiter."""
        self.limiter_enabled = no
        if enabled:
            print("? Limiter W??CZONY")
        else:
            print("? Limiter WY??CZONY")

    def get_most_recent_file(self):
        """Znajduje najnowszy folder w 'graphs/' i wyszukuje w nim plik JSON o tej samej nazwie."""
        folders = [f for f in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, f))]
        if not folders:
            raise FileNotFoundError("Brak foldw w katalogu 'graphs/'")

        latest_folder = max(folders, key=lambda f: os.path.getctime(os.path.join(self.directory, f)))
        folder_path = os.path.join(self.directory, latest_folder)

        json_file_path = os.path.join(folder_path, f"{latest_folder}.json")
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku {latest_folder}.json w folderze {folder_path}")

        return json_file_path

    def force_check(self, limit=None):
        """Sprawdza, czy w przeci?gu ostatnich `limit` sekund warto?? force si? zmieni?a."""

        # ? Je?li limiter jest wy??czony, zawsze zwracamy True
        if not self.limiter_enabled:
            return True

        if limit is None:
            limit = self.default_limit
        recent_file = self.get_most_recent_file()

        with open(recent_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if "force" not in data or "seconds" not in data:
            raise KeyError("Brak klucza 'force' lub 'seconds' w danych JSON.")

        force_values = [float(value.replace(" ", "").replace("N", "")) for value in data["force"]]
        time_values = data["seconds"]

        if len(force_values) != len(time_values):
            raise ValueError("Nieprawid?owa d?ugo?? list w danych JSON.")

        current_time = time_values[-1]
        latest_force = force_values[-1]

        for i in range(len(time_values) - 1, -1, -1):
            if current_time - time_values[i] > limit:
                break  

            if force_values[i] != latest_force:
                return True  

        return False  
