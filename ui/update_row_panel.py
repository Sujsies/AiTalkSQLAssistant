# aitalk_sql_assistant/ui/update_row_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

class UpdateRowPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.update_entries = {}

        ctk.CTkLabel(self, text="Update Row", font=ctk.CTkFont(weight="bold")).pack(pady=4)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", pady=4, padx=6)
        ctk.CTkLabel(top, text="Table:").pack(side="left", padx=6)

        tables = self.app.db_manager.fetch_tables()
        self.table_var = tk.StringVar(value=tables[0] if tables else "")
        table_menu = ttk.Combobox(top, textvariable=self.table_var, values=tables)
        table_menu.pack(side="left", padx=6)
        table_menu.bind("<<ComboboxSelected>>", self.load_columns_event)
        
        ctk.CTkButton(top, text="Load Columns", command=self.load_columns_event).pack(side="left", padx=6)

        self.cols_area = ctk.CTkScrollableFrame(self)
        self.cols_area.pack(fill="both", expand=True, padx=6, pady=6)

        where_frame = ctk.CTkFrame(self)
        where_frame.pack(fill="x", padx=6, pady=4)
        ctk.CTkLabel(where_frame, text="WHERE clause:").pack(side="left", padx=6)
        self.where_entry = ctk.CTkEntry(where_frame)
        self.where_entry.pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkButton(self, text="Submit Update", command=self.submit_update).pack(pady=6)

    def load_columns_event(self, event=None):
        table = self.table_var.get()
        for w in self.cols_area.winfo_children(): w.destroy()
        cols = self.app.db_manager.fetch_columns(table)
        self.update_entries = {}
        for col in cols:
            row = ctk.CTkFrame(self.cols_area)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=col, width=150, anchor="w").pack(side="left", padx=6)
            ent = ctk.CTkEntry(row)
            ent.pack(side="left", fill="x", expand=True, padx=6)
            self.update_entries[col] = ent
            
    def submit_update(self):
        table = self.table_var.get()
        if not table: return

        sets = []
        for col, ent in self.update_entries.items():
            v = ent.get().strip()
            if v:
                safe_val = "'" + v.replace("'", "''") + "'"
                sets.append(f"`{col}`={safe_val}")

        if not sets:
            messagebox.showwarning("Update", "No values provided to SET.")
            return

        where = self.where_entry.get().strip()
        if not where and not messagebox.askyesno("Confirm", "No WHERE clause. This will update all rows. Continue?"):
            return
            
        query = f"UPDATE `{table}` SET {', '.join(sets)}"
        if where:
            query += f" WHERE {where}"

        self.app.execute_sql_query(query)
