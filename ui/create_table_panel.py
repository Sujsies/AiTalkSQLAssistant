# aitalk_sql_assistant/ui/create_table_panel.py

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class CreateTablePanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.column_rows = []

        ctk.CTkLabel(self, text="Create Table (free form)", font=ctk.CTkFont(weight="bold")).pack(pady=4)

        self.tname_entry = ctk.CTkEntry(self, placeholder_text="Table Name")
        self.tname_entry.pack(pady=6, padx=6)

        self.cols_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cols_frame.pack(fill="x", pady=4, padx=4)
        
        ctk.CTkButton(self, text="Add Column", command=self.add_column_row).pack(pady=6)
        ctk.CTkButton(self, text="Create Table", command=self.submit_create).pack(pady=8)
        
        self.add_column_row()

    def add_column_row(self):
        row_widgets = {}
        row_frame = ctk.CTkFrame(self.cols_frame)
        row_frame.pack(fill="x", pady=4, padx=4)

        name_entry = ctk.CTkEntry(row_frame, placeholder_text="Column Name")
        name_entry.pack(side="left", padx=6, expand=True, fill="x")
        type_entry = ctk.CTkEntry(row_frame, placeholder_text="Data Type (e.g., INT, TEXT)")
        type_entry.pack(side="left", padx=6, expand=True, fill="x")

        # --- NEW: Added "Not Null" checkbox ---
        not_null_var = tk.BooleanVar()
        not_null_check = ctk.CTkCheckBox(row_frame, text="Not Null", variable=not_null_var, width=100)
        not_null_check.pack(side="left", padx=6)

        pk_var = tk.BooleanVar()
        fk_var = tk.BooleanVar()
        ref_table_entry = ctk.CTkEntry(row_frame, placeholder_text="Ref. Table")
        ref_col_entry = ctk.CTkEntry(row_frame, placeholder_text="Ref. Column")

        def on_pk_select():
            if pk_var.get():
                fk_var.set(False)
                ref_table_entry.pack_forget()
                ref_col_entry.pack_forget()

        def on_fk_select():
            if fk_var.get():
                pk_var.set(False)
            if fk_var.get():
                ref_table_entry.pack(side="left", padx=6, expand=True, fill="x")
                ref_col_entry.pack(side="left", padx=6, expand=True, fill="x")
            else:
                ref_table_entry.pack_forget()
                ref_col_entry.pack_forget()

        pk_check = ctk.CTkCheckBox(row_frame, text="PK", variable=pk_var, width=50, command=on_pk_select)
        pk_check.pack(side="left", padx=6)
        
        fk_check = ctk.CTkCheckBox(row_frame, text="FK", variable=fk_var, width=50, command=on_fk_select)
        fk_check.pack(side="left", padx=6)

        row_widgets.update({
            "name": name_entry, "type": type_entry,
            "not_null_var": not_null_var, # Storing the new checkbox variable
            "pk_var": pk_var, "fk_var": fk_var,
            "ref_table": ref_table_entry, "ref_col": ref_col_entry
        })
        self.column_rows.append(row_widgets)
        on_fk_select()

    def submit_create(self):
        tname = self.tname_entry.get().strip()
        if not tname:
            messagebox.showwarning("Create Table", "Table name is required.")
            return

        col_definitions, primary_keys, foreign_keys = [], [], []

        for row in self.column_rows:
            cname = row['name'].get().strip()
            ctype = row['type'].get().strip()

            if cname and ctype:
                # --- NEW: Append "NOT NULL" to the definition if checked ---
                col_def = f"`{cname}` {ctype}"
                if row['not_null_var'].get():
                    col_def += " NOT NULL"
                col_definitions.append(col_def)
                
                if row['pk_var'].get():
                    primary_keys.append(f"`{cname}`")
                
                if row['fk_var'].get():
                    ref_table = row['ref_table'].get().strip()
                    ref_col = row['ref_col'].get().strip()
                    if ref_table and ref_col:
                        fk_def = f"FOREIGN KEY (`{cname}`) REFERENCES `{ref_table}`(`{ref_col}`)"
                        foreign_keys.append(fk_def)

        if not col_definitions:
            messagebox.showwarning("Create Table", "At least one valid column is required.")
            return

        all_parts = col_definitions
        if primary_keys:
            all_parts.append(f"PRIMARY KEY ({', '.join(primary_keys)})")
        all_parts.extend(foreign_keys)

        query_body = ", ".join(all_parts)
        query = f"CREATE TABLE `{tname}` ({query_body})"
        
        self.app.execute_sql_query(query)
