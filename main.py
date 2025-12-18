# aitalk_sql_assistant/main.py

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import customtkinter as ctk
import time

# App components
from core.db_manager import DBManager
from core.history_manager import HistoryManager
from core.speech_handler import SpeechHandler
import core.exporter as exporter
import config

# UI Panels
from ui.connection_panel import ConnectionPanel
from ui.insert_row_panel import InsertRowPanel
from ui.update_row_panel import UpdateRowPanel
from ui.delete_row_panel import DeleteRowPanel
from ui.create_table_panel import CreateTablePanel
from ui.drop_table_panel import DropTablePanel
from ui.view_data_panel import ViewDataPanel

class AITalkApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_NAME)
        self.root.geometry(config.INITIAL_GEOMETRY)

        self.db_manager = DBManager()
        self.history_manager = HistoryManager()
        self.speech_handler = SpeechHandler()
        self.status_var = tk.StringVar(value="Disconnected")

        self._setup_ui()
        self.setup_enter_navigation()
        self._update_ui_state() 

    def _setup_ui(self):
        self._setup_menubar()

        self.left_frame = ctk.CTkFrame(self.root, width=300)
        self.left_frame.pack(side="left", fill="y", padx=8, pady=8)
        self.left_frame.pack_propagate(False)
        self.connection_panel = ConnectionPanel(self.left_frame, self)
        self.connection_panel.pack(fill="x", pady=(0, 10))
        ctk.CTkButton(self.left_frame, text="Connect", command=self.connect_db).pack(pady=4, fill="x", padx=6)
        ctk.CTkButton(self.left_frame, text="Disconnect", fg_color="orange", hover_color="darkorange", command=self.disconnect_db).pack(pady=4, fill="x", padx=6)
        self.status_label = ctk.CTkLabel(self.left_frame, textvariable=self.status_var, text_color="orange")
        self.status_label.pack(pady=8)
        
        self.right_panel = ctk.CTkFrame(self.root)
        self.right_panel.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=8)

        topbar = ctk.CTkFrame(self.right_panel)
        topbar.pack(fill="x", padx=6, pady=6)
        ctk.CTkLabel(topbar, text="AI Interaction / SQL", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=6)
        actions_frame = ctk.CTkFrame(topbar)
        actions_frame.pack(side="right")
        ctk.CTkButton(actions_frame, text="Export Results", width=120, command=self.export_results).pack(side="left", padx=4)
        ctk.CTkButton(actions_frame, text="Export History", width=120, command=self.export_history).pack(side="left", padx=4)
        ctk.CTkButton(actions_frame, text="Refresh", width=100, command=self.refresh_app).pack(side="left", padx=4)
        ctk.CTkButton(actions_frame, text="Dark Mode", width=100 ,command=self.toggle_dark_mode).pack(side="left", padx=4)

        query_frame = ctk.CTkFrame(self.right_panel)
        query_frame.pack(fill="x", padx=6, pady=4)
        self.query_entry = ctk.CTkEntry(query_frame, placeholder_text="Type your SQL query or natural language command...")
        self.query_entry.pack(side="left", fill="x", expand=True, padx=(6, 4))
        self.query_entry.bind("<Return>", lambda e: self.text_query())
        self.text_query_button = ctk.CTkButton(query_frame, text="Text Query", command=self.text_query, width=120)
        self.text_query_button.pack(side="left", padx=4)
        self.speak_query_button = ctk.CTkButton(query_frame, text="Speak Query", command=self.speak_query, width=120)
        self.speak_query_button.pack(side="left", padx=4)
        
        self.output_box = ctk.CTkTextbox(self.right_panel, height=100)
        self.output_box.pack(fill="x", padx=6, pady=(0, 6))

        self.panel_area = ctk.CTkFrame(self.right_panel, height=240)
        self.panel_area.pack(fill="x", expand=False, padx=6, pady=6)
        self.panel_area.pack_propagate(False)
        
        tree_frame = ctk.CTkFrame(self.right_panel)
        tree_frame.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.result_tree = ttk.Treeview(tree_frame, show="headings")
        self.result_tree.pack(side="left", fill="both", expand=True)
        self._update_treeview_style()

    def _setup_menubar(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="My Schemas", command=self.show_schemas_window)
        file_menu.add_separator()
        file_menu.add_command(label="Export History", command=self.export_history)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        self.menubar.add_cascade(label="File", menu=file_menu)
        history_menu = tk.Menu(self.menubar, tearoff=0)
        history_menu.add_command(label="View History", command=self.show_history_window)
        history_menu.add_command(label="Clear History", command=self.clear_history)
        self.menubar.add_cascade(label="History", menu=history_menu)
        self.db_menu = tk.Menu(self.menubar, tearoff=0)
        self.db_menu.add_command(label="View/Plot Data", command=lambda: self.show_db_function("view"))
        self.db_menu.add_command(label="Insert Row", command=lambda: self.show_db_function("insert"))
        self.db_menu.add_command(label="Update Row", command=lambda: self.show_db_function("update"))
        self.db_menu.add_command(label="Delete Row(s)", command=lambda: self.show_db_function("delete"))
        self.db_menu.add_separator()
        self.db_menu.add_command(label="Create Table", command=lambda: self.show_db_function("create"))
        self.db_menu.add_command(label="Drop Table", command=lambda: self.show_db_function("drop"))
        self.menubar.add_cascade(label="Database", menu=self.db_menu)

    def _update_ui_state(self):
        is_connected = self.db_manager.is_connected()
        new_state = "normal" if is_connected else "disabled"
        if self.text_query_button: self.text_query_button.configure(state=new_state)
        if self.speak_query_button: self.speak_query_button.configure(state=new_state)
        if self.menubar: self.menubar.entryconfig("Database", state=new_state)

    # --- THIS METHOD IS NOW FULLY UPDATED ---
    def connect_db(self):
        params = self.connection_panel.get_connection_params()
        db_type = params.get('db_type')
        db_name = params.get('database', '').strip()

        # 1. Check if the database field is compulsory and empty
        if db_type in ("MySQL", "PostgreSQL") and not db_name:
            messagebox.showwarning("Input Required", "The 'Database' field cannot be empty.")
            return

        # 2. First connection attempt
        status, error = self.db_manager.connect(db_type, params)
        
        if error:
            # 3. Check for the specific "database doesn't exist" error
            is_mysql_unknown_db = (db_type == "MySQL" and hasattr(error, 'errno') and error.errno == 1049)
            is_pg_unknown_db = (db_type == "PostgreSQL" and "does not exist" in str(error))

            if is_mysql_unknown_db or is_pg_unknown_db:
                # 4. Ask the user if they want to create it
                if messagebox.askyesno("Database Not Found", f"The database '{db_name}' does not exist.\nWould you like to create it?"):
                    
                    # 5. Call the create_database method
                    create_status, create_error = self.db_manager.create_database(db_type, params, db_name)
                    if create_error:
                        messagebox.showerror("Creation Failed", f"Could not create database:\n{create_error}")
                        return
                    
                    messagebox.showinfo("Success", create_status)
                    
                    # 6. Try connecting again now that the database exists
                    status, error = self.db_manager.connect(db_type, params)
                else:
                    return # User chose not to create the database

        # 7. Final status check after all attempts
        if error:
            messagebox.showerror("Connection Error", str(error))
            self.speech_handler.speak("Failed to connect")
        else:
            self.status_var.set(status)
            self.status_label.configure(text_color="green")
            self.speech_handler.speak("Connected to database")

        self._update_ui_state()

    def disconnect_db(self):
        self.db_manager.disconnect()
        self.status_var.set("Disconnected")
        self.status_label.configure(text_color="orange")
        self.speech_handler.speak("Disconnected")
        self.show_db_function(None)
        self._update_ui_state()

    def setup_enter_navigation(self):
        widgets = self.connection_panel.get_ordered_entries()
        self._bind_enter_navigation(widgets, final_action=self.connect_db)
        
    def _bind_enter_navigation(self, widgets, final_action=None):
        for i, widget in enumerate(widgets):
            if i < len(widgets) - 1 and widget is not None:
                widget.bind("<Return>", lambda e, w=widgets[i+1]: w.focus())
            elif final_action and widget is not None:
                widget.bind("<Return>", lambda e: final_action())

    def toggle_dark_mode(self):
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode.lower() == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)
        self._update_treeview_style()

    def _update_treeview_style(self):
        style = ttk.Style()
        style.theme_use("default")
        bg_color = self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])
        heading_bg = self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        style.configure("Treeview", background=bg_color, foreground=text_color, fieldbackground=bg_color, borderwidth=0)
        style.map("Treeview", background=[("selected", ctk.ThemeManager.theme["CTkButton"]["fg_color"])])
        style.configure("Treeview.Heading", background=heading_bg, foreground=text_color, relief="flat")
        style.map("Treeview.Heading", background=[("active", ctk.ThemeManager.theme["CTkButton"]["hover_color"])])

    def refresh_app(self):
        self.show_db_function(None)
        self.output_box.insert("end", "UI Refreshed.\n")

    def execute_sql_query(self, query):
        if not self.db_manager.is_connected():
            messagebox.showwarning("No Connection", "Please connect to a database first.")
            return
        try:
            rows, cols = self.db_manager.run_sql(query)
            self.history_manager.add_item(query)
            if rows is not None and cols is not None:
                self.show_results(rows, cols)
                self.speech_handler.speak(f"Query executed. {len(rows)} rows returned.")
            else:
                self.output_box.insert("end", f"Executed: {query}\n")
                self.speech_handler.speak("Query executed")
                self.clear_treeview() 
            if query.strip().lower().startswith(("create", "drop", "alter", "truncate")):
                self.show_db_function(None)
        except Exception as e:
            messagebox.showerror("SQL Error", str(e))
            self.speech_handler.speak("Error executing query")

    def show_results(self, rows, cols):
        self.clear_treeview()
        if not cols: return
        self.result_tree["columns"] = cols
        for col in cols:
            self.result_tree.heading(col, text=col, anchor="w")
            self.result_tree.column(col, width=120, anchor="w")
        for r in rows:
            vals = [("" if v is None else str(v)) for v in r]
            self.result_tree.insert("", "end", values=vals)

    def clear_treeview(self):
        self.result_tree.delete(*self.result_tree.get_children())
        self.result_tree["columns"] = ()

    def text_query(self):
        if q := self.query_entry.get().strip(): self.execute_sql_query(q)

    def speak_query(self):
        self.speech_handler.speak("Listening now.")
        self.output_box.insert("end", "Listening...\n")
        self.root.update_idletasks()
        query, error = self.speech_handler.listen_for_query()
        if error: self.output_box.insert("end", f"Error: {error}\n")
        if query:
            self.output_box.insert("end", f"You said: {query}\n")
            self.query_entry.delete(0, "end")
            self.query_entry.insert(0, query)
            self.execute_sql_query(query)

    def show_history_window(self):
        history_win = ctk.CTkToplevel(self.root)
        history_win.title("Query History")
        history_win.geometry("600x400")
        text = ctk.CTkTextbox(history_win, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        for item in self.history_manager.get_history():
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item.get("ts", 0)))
            text.insert("end", f"[{ts}]  {item.get('query')}\n")

    def clear_history(self):
        if messagebox.askyesno("Clear History", "Clear all local history?"):
            self.history_manager.clear()
            messagebox.showinfo("History", "History cleared.")

    def export_history(self):
        exporter.export_history_to_file(self.history_manager.get_history())

    def export_results(self):
        if not self.result_tree.get_children():
            messagebox.showinfo("Export", "There is no data to export.")
            return
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Export Format")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set() 

        label = ctk.CTkLabel(dialog, text="Choose an export format:")
        label.pack(pady=20)

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack()

        def export_and_close(export_function):
            dialog.destroy()
            export_function(self.result_tree)

        pdf_button = ctk.CTkButton(
            button_frame, text="PDF (Table)",
            command=lambda: export_and_close(exporter.export_data_to_pdf)
        )
        pdf_button.pack(side="left", padx=10)
        csv_button = ctk.CTkButton(
            button_frame, text="CSV (Spreadsheet)",
            command=lambda: export_and_close(exporter.export_data_to_csv)
        )
        csv_button.pack(side="left", padx=10)

    def show_schemas_window(self):
        if not self.db_manager.is_connected():
            messagebox.showwarning("Not Connected", "Please connect to a database to view schemas.")
            return
        schemas_win = ctk.CTkToplevel(self.root)
        schemas_win.title("My Schemas")
        schemas_win.geometry("800x500")
        schemas_win.transient(self.root)
        self._populate_schemas_with_tables(schemas_win)

    def _populate_schemas_with_tables(self, win):
        for widget in win.winfo_children(): widget.destroy()
        win.title("My Schemas - Select a Table")
        tables = self.db_manager.fetch_tables()
        if not tables:
            ctk.CTkLabel(win, text="No tables found in the database.").pack(pady=20)
            return
        scroll_frame = ctk.CTkScrollableFrame(win, label_text="Tables")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        for table_name in tables:
            btn = ctk.CTkButton(scroll_frame, text=table_name, command=lambda t=table_name: self._populate_schemas_with_info(win, t))
            btn.pack(fill="x", padx=10, pady=4)

    def _populate_schemas_with_info(self, win, table_name):
        for widget in win.winfo_children(): widget.destroy()
        win.title(f"Schema for: {table_name}")
        top_frame = ctk.CTkFrame(win)
        top_frame.pack(fill="x", padx=10, pady=(10, 0))
        back_button = ctk.CTkButton(top_frame, text="< Back to Tables", command=lambda: self._populate_schemas_with_tables(win))
        back_button.pack(side="left")
        try:
            rows, headers = self.db_manager.fetch_table_info(table_name)
            tree = ttk.Treeview(win, columns=headers, show="headings")
            tree.pack(fill="both", expand=True, padx=10, pady=10)
            for header in headers:
                tree.heading(header, text=header)
                tree.column(header, anchor="w", width=120)
            for row in rows:
                tree.insert("", "end", values=[("" if v is None else v) for v in row])
        except Exception as e:
            ctk.CTkLabel(win, text=f"Could not fetch table info:\n{e}", text_color="red").pack(pady=20)
            
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Exit application now?"):
            self.history_manager.save_to_disk()
            self.disconnect_db()
            self.root.destroy()
            
    def show_db_function(self, func_name):
        for widget in self.panel_area.winfo_children(): widget.destroy()
        if not self.db_manager.is_connected():
            if func_name: messagebox.showwarning("Not Connected", "Please connect to a database first.")
            return
        panel_map = {
            "view": ViewDataPanel, "insert": InsertRowPanel, "update": UpdateRowPanel,
            "delete": DeleteRowPanel, "create": CreateTablePanel, "drop": DropTablePanel,
        }
        if panel_class := panel_map.get(func_name):
            panel = panel_class(self.panel_area, self)
            panel.pack(fill="both", expand=True)
