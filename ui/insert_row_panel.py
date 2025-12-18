# aitalk_sql_assistant/ui/insert_row_panel.py

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

class InsertRowPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.insert_entries = {}

        ctk.CTkLabel(self, text="Insert Row", font=ctk.CTkFont(weight="bold")).pack(pady=4)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", pady=4, padx=6)
        ctk.CTkLabel(top, text="Table:").pack(side="left", padx=6)
        
        tables = self.app.db_manager.fetch_tables()
        self.table_var = tk.StringVar(value=tables[0] if tables else "")
        table_menu = ttk.Combobox(top, textvariable=self.table_var, values=tables)
        table_menu.pack(side="left", padx=6)

        table_menu.bind("<<ComboboxSelected>>", self.load_columns_event)
        table_menu.bind("<Return>", self.load_columns_event)
        ctk.CTkButton(top, text="Load Columns", command=self.load_columns_event).pack(side="left", padx=6)

        self.cols_area = ctk.CTkScrollableFrame(self)
        self.cols_area.pack(fill="both", expand=True, padx=6, pady=6)

        ctk.CTkButton(self, text="Submit Insert", command=self.submit_insert).pack(pady=6)

    def load_columns_event(self, event=None):
        table = self.table_var.get()
        for w in self.cols_area.winfo_children(): w.destroy()
        if not table: return

        cols = self.app.db_manager.fetch_columns(table)
        self.insert_entries = {}
        for col in cols:
            row = ctk.CTkFrame(self.cols_area)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=col, width=150, anchor="w").pack(side="left", padx=6)
            ent = ctk.CTkEntry(row)
            ent.pack(side="left", fill="x", expand=True, padx=6)
            self.insert_entries[col] = ent
    
    def submit_insert(self):
        table = self.table_var.get()
        if not table: return

        cols, vals = [], []
        for col, ent in self.insert_entries.items():
            v = ent.get().strip()
            if v:
                cols.append(f"`{col}`")
                vals.append("'" + v.replace("'", "''") + "'") # Basic SQL injection prevention
        
        if not cols:
            messagebox.showwarning("Insert", "No values provided.")
            return

        query = f"INSERT INTO `{table}` ({', '.join(cols)}) VALUES ({', '.join(vals)})"
        self.app.execute_sql_query(query)
