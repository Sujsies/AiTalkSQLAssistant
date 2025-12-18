# aitalk_sql_assistant/ui/drop_table_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

class DropTablePanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        ctk.CTkLabel(self, text="Drop Table", font=ctk.CTkFont(weight="bold")).pack(pady=10)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", pady=10, padx=6)
        ctk.CTkLabel(top, text="Table to Drop:").pack(side="left", padx=6)

        tables = self.app.db_manager.fetch_tables()
        self.table_var = tk.StringVar(value=tables[0] if tables else "")
        ttk.Combobox(top, textvariable=self.table_var, values=tables).pack(side="left", padx=6)

        ctk.CTkButton(self, text="Drop Table", command=self.submit_drop, fg_color="red", hover_color="darkred").pack(pady=20)

    def submit_drop(self):
        table = self.table_var.get()
        if not table:
            messagebox.showwarning("Drop", "Table not specified.")
            return
        
        if not messagebox.askyesno("Confirm Drop", f"Are you sure you want to permanently delete the table '{table}'? This cannot be undone."):
            return

        query = f"DROP TABLE `{table}`"
        self.app.execute_sql_query(query)
