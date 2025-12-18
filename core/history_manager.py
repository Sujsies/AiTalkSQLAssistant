# aitalk_sql_assistant/core/history_manager.py

import os
import json
import time
from config import HISTORY_FILE_PATH

class HistoryManager:
    def __init__(self):
        self.history = []
        self.load_from_disk()

    def load_from_disk(self):
        try:
            if os.path.exists(HISTORY_FILE_PATH):
                with open(HISTORY_FILE_PATH, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self.history = []

    def save_to_disk(self):
        try:
            with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            print("Error: Could not save history to disk.")

    def add_item(self, query_text):
        item = {"ts": int(time.time()), "query": str(query_text)}
        self.history.append(item)
        self.save_to_disk()

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
        if os.path.exists(HISTORY_FILE_PATH):
            os.remove(HISTORY_FILE_PATH)
