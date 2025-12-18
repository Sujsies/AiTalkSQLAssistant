# aitalk_sql_assistant/ui/delete_row_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

class DeleteRowPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        ctk.CTkLabel(self, text="Delete Row(s)", font=ctk.CTkFont(weight="bold")).pack(pady=4)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", pady=10, padx=6)
        ctk.CTkLabel(top, text="Table:").pack(side="left", padx=6)
        
        tables = self.app.db_manager.fetch_tables()
        self.table_var = tk.StringVar(value=tables[0] if tables else "")
        ttk.Combobox(top, textvariable=self.table_var, values=tables).pack(side="left", padx=6)

        where_frame = ctk.CTkFrame(self)
        where_frame.pack(fill="x", padx=6, pady=4)
        ctk.CTkLabel(where_frame, text="WHERE clause:").pack(side="left", padx=6)
        self.where_entry = ctk.CTkEntry(where_frame, placeholder_text="e.g., id = 5")
        self.where_entry.pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkButton(self, text="Submit Delete", command=self.submit_delete, fg_color="red", hover_color="darkred").pack(pady=10)

    def submit_delete(self):
        table = self.table_var.get()
        if not table:
            messagebox.showwarning("Delete", "Table not specified.")
            return

        where = self.where_entry.get().strip()
        if not where:
            if not messagebox.askyesno("Confirm", "No WHERE clause specified. This will DELETE ALL ROWS from the table. Are you absolutely sure?"):
                return
        
        query = f"DELETE FROM `{table}`"
        if where:
            query += f" WHERE {where}"

        self.app.execute_sql_query(query)
