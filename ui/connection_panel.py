# aitalk_sql_assistant/ui/connection_panel.py

import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from config import SUPPORTED_DATABASES

class ConnectionPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.conn_entries = {}
        
        # --- CHANGE 1: Create a variable to hold the checkbox state ---
        self.show_password_var = tk.BooleanVar(value=False)

        ctk.CTkLabel(self, text="Database Connection", font=ctk.CTkFont(weight="bold")).pack(pady=5)

        self.db_type_var = tk.StringVar(value=SUPPORTED_DATABASES[0])
        ctk.CTkOptionMenu(self, variable=self.db_type_var, values=SUPPORTED_DATABASES,
                          command=self.on_db_type_change).pack(pady=5, fill="x", padx=7)

        self.fields_container = ctk.CTkFrame(self)
        self.fields_container.pack(fill="x", pady=2, padx=6)

        self.build_connection_fields(self.db_type_var.get())

    def on_db_type_change(self, db_type):
        self.build_connection_fields(db_type)
        self.app.setup_enter_navigation()

    def build_connection_fields(self, db_type):
        for w in self.fields_container.winfo_children():
            w.destroy()
        self.conn_entries.clear()

        if db_type in ("MySQL", "PostgreSQL"):
            self.fields_container.grid_columnconfigure(1, weight=1)
            
            labels = {"Host:": "host", "User:": "user", "Password:": "password", "Database:": "database"}
            placeholders = {"host": "localhost", "user": "root", "password": "", "database": "your_db"}
            
            for i, (label_text, key) in enumerate(labels.items()):
                lbl = ctk.CTkLabel(self.fields_container, text=label_text)
                lbl.grid(row=i, column=0, sticky="w", padx=2, pady=4)
                
                show_char = "*" if key == "password" else ""
                entry = ctk.CTkEntry(self.fields_container, placeholder_text=placeholders[key], show=show_char)
                entry.grid(row=i, column=1, sticky="ew", padx=2, pady=4)
                self.conn_entries[key] = entry

            # --- CHANGE 2: Link the checkbox to the variable ---
            chk = ctk.CTkCheckBox(self.fields_container, text="Show Password",
                                  variable=self.show_password_var,  # Link to the variable
                                  command=self._toggle_password_visibility)
            chk.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=(2, 6))

        elif db_type == "SQLite":
            self.fields_container.grid_columnconfigure(0, weight=1)
            db_entry = ctk.CTkEntry(self.fields_container, placeholder_text="Path to .db file")
            db_entry.grid(row=0, column=0, sticky="ew", padx=2, pady=4)
            browse = ctk.CTkButton(self.fields_container, text="Browse", command=self._browse_sqlite, width=80)
            browse.grid(row=0, column=1, padx=2, pady=4)
            self.conn_entries["database"] = db_entry

    # --- CHANGE 3: Update the logic to use the variable ---
    def _toggle_password_visibility(self):
        """Toggles the visibility of the password entry field based on the checkbox state."""
        password_entry = self.conn_entries.get("password")
        if password_entry:
            # If the variable is True (box is checked), show the password
            if self.show_password_var.get():
                password_entry.configure(show="")
            # Otherwise (box is unchecked), hide the password
            else:
                password_entry.configure(show="*")

    def _browse_sqlite(self):
        path = filedialog.askopenfilename(title="Select SQLite DB", filetypes=[("SQLite DB", "*.db"), ("All files", "*.*")])
        if path and "database" in self.conn_entries:
            self.conn_entries["database"].delete(0, "end")
            self.conn_entries["database"].insert(0, path)

    def get_connection_params(self):
        params = {"db_type": self.db_type_var.get()}
        for key, widget in self.conn_entries.items():
            if isinstance(widget, ctk.CTkEntry):
                params[key] = widget.get().strip()
        return params

    def get_ordered_entries(self):
        """Returns the entry widgets in their visual order for navigation."""
        if self.db_type_var.get() in ("MySQL", "PostgreSQL"):
            return [
                self.conn_entries.get("host"),
                self.conn_entries.get("user"),
                self.conn_entries.get("password"),
                self.conn_entries.get("database"),
            ]
        else: # SQLite
            return [self.conn_entries.get("database")]
