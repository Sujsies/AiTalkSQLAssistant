# aitalk_sql_assistant/ui/view_data_panel.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import matplotlib.pyplot as plt

class ViewDataPanel(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        ctk.CTkLabel(self, text="View & Plot Data", font=ctk.CTkFont(weight="bold")).pack(pady=4)

        tables = self.app.db_manager.fetch_tables()
        self.table_var = tk.StringVar(value=tables[0] if tables else "")
        
        view_frame = ctk.CTkFrame(self)
        view_frame.pack(fill="x", pady=4, padx=6)
        ctk.CTkLabel(view_frame, text="Table:").pack(side="left", padx=6)
        table_menu = ttk.Combobox(view_frame, textvariable=self.table_var, values=tables)
        table_menu.pack(side="left", padx=6)
        table_menu.bind("<<ComboboxSelected>>", self.refresh_plot_columns)
        ctk.CTkButton(view_frame, text="View Data", command=self.do_view).pack(side="left", padx=6)

        plot_frame = ctk.CTkFrame(self, fg_color="transparent")
        plot_frame.pack(fill="x", pady=6, padx=6)
        
        self.plot_type_var = tk.StringVar(value="bar")
        self.xcol_var = tk.StringVar()
        self.ycol_var = tk.StringVar()

        ctk.CTkLabel(plot_frame, text="Plot:").pack(side="left", padx=6)
        ctk.CTkOptionMenu(plot_frame, variable=self.plot_type_var, values=["bar", "line", "scatter", "pie"]).pack(side="left", padx=3)
        ctk.CTkLabel(plot_frame, text="X:").pack(side="left", padx=(10,0))
        self.xcol_cb = ttk.Combobox(plot_frame, textvariable=self.xcol_var, width=15)
        self.xcol_cb.pack(side="left", padx=3)
        ctk.CTkLabel(plot_frame, text="Y:").pack(side="left", padx=(10,0))
        self.ycol_cb = ttk.Combobox(plot_frame, textvariable=self.ycol_var, width=15)
        self.ycol_cb.pack(side="left", padx=3)

        ctk.CTkButton(plot_frame, text="Plot Data", command=self.plot_data).pack(side="left", padx=6)
        # --- ADDED: "Save Chart" button ---
        ctk.CTkButton(plot_frame, text="Save Chart", command=self.save_plot).pack(side="left", padx=6)

        self.refresh_plot_columns()

    def do_view(self):
        if table := self.table_var.get():
            self.app.execute_sql_query(f"SELECT * FROM `{table}`")

    def refresh_plot_columns(self, event=None):
        table = self.table_var.get()
        cols = self.app.db_manager.fetch_columns(table) if table else []
        self.xcol_cb['values'] = cols
        self.ycol_cb['values'] = cols
        self.xcol_var.set(cols[0] if cols else "")
        self.ycol_var.set(cols[1] if len(cols) > 1 else "")

    def _generate_plot(self, for_saving=False):
        """Helper function to generate a plot. Returns True on success."""
        table, xcol, ycol = self.table_var.get(), self.xcol_var.get(), self.ycol_var.get()
        if not all([table, xcol, ycol]):
            messagebox.showwarning("Plot Error", "Table, X column, and Y column must be selected.")
            return False

        try:
            rows, _ = self.app.db_manager.run_sql(f"SELECT `{xcol}`, `{ycol}` FROM `{table}`")
            if not rows: 
                if not for_saving: messagebox.showinfo("Plot", "No data to plot.")
                return False

            x_data = [row[0] for row in rows]
            y_data = [float(row[1]) for row in rows] 

            plt.figure(figsize=(8, 6)) # Create a new figure
            plot_type = self.plot_type_var.get()

            if plot_type == "bar": plt.bar(x_data, y_data)
            elif plot_type == "line": plt.plot(x_data, y_data)
            elif plot_type == "scatter": plt.scatter(x_data, y_data)
            elif plot_type == "pie":
                plt.pie(y_data, labels=x_data, autopct='%1.1f%%', startangle=90)
                plt.axis('equal')

            plt.title(f"{ycol} vs {xcol} from {table}")
            plt.xlabel(xcol)
            plt.ylabel(ycol)
            plt.tight_layout()
            return True
        except (ValueError, TypeError):
             messagebox.showerror("Plot Error", "Plotting failed. Y-axis column must contain numeric data.")
             return False
        except Exception as e:
            messagebox.showerror("Plot Error", str(e))
            return False

    def plot_data(self):
        """Generates and shows the plot in a window."""
        if self._generate_plot():
            plt.show()

    def save_plot(self):
        """Generates and saves the plot to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Chart As"
        )
        if not file_path: return
        
        if self._generate_plot(for_saving=True):
            try:
                plt.savefig(file_path, dpi=300)
                plt.close() # Close the figure to free memory
                messagebox.showinfo("Success", f"Chart saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save chart:\n{e}")
