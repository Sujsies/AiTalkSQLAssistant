import customtkinter as ctk
from main import AITalkApp
import config
import os
import sys

# --- ADD THIS HELPER FUNCTION ---
# This function creates the correct path for assets, whether running from source or as a .exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    """
    Main entry point for the application.
    """
    ctk.set_appearance_mode(config.INITIAL_THEME)
    
    root = ctk.CTk()
    
    # --- THIS LINE HAS BEEN UPDATED ---
    # It now uses the helper function to find the icon file.
    root.iconbitmap(resource_path("assets/icon.ico"))
    
    app = AITalkApp(root)
    
    # Set the close protocol to handle the exit properly
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    
    root.mainloop()
