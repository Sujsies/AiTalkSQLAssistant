# aitalk_sql_assistant/config.py

import os


# --- Application Settings ---
APP_NAME = "AI Talk - SQL Assistant"
INITIAL_GEOMETRY = "1200x700"
INITIAL_THEME = "light" # "light", "dark", or "system"

# --- History File ---
HISTORY_FILE_NAME = ".aitalk_history.json"
HISTORY_FILE_PATH = os.path.join(os.path.expanduser("~"), HISTORY_FILE_NAME)

# --- Database Options ---
SUPPORTED_DATABASES = ["MySQL", "SQLite", "PostgreSQL"]
