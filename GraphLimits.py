import json
import os

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
        if limit is None:
            limit = self.default_limit
        recent_file = self.get_most_recent_file()
        with open(recent_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Access the 'force' values correctly
        force_key = [key for key, value in data.items() if isinstance(value, dict) and 'key' in value and value['key'] == 'force']
        if not force_key:
            raise KeyError("No 'force' key found in the JSON data")
        
        force_values = data[force_key[0]]['values']
        
        exceeding_indices = [i for i, force in enumerate(force_values) if force > limit]
        return len(exceeding_indices) > 0