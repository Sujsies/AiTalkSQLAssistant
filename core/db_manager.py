# aitalk_sql_assistant/core/db_manager.py

import mysql.connector
import sqlite3
import psycopg2

class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.db_type = ""
        self.db_name = ""

    def connect(self, db_type, params):
        self.disconnect()  
        self.db_type = db_type
        self.db_name = params.get("database", "").split('/')[-1].split('\\')[-1]
        
        try:
            if db_type == "MySQL":
                self.conn = mysql.connector.connect(
                    host=params.get('host'), user=params.get('user'),
                    password=params.get('password'), database=params.get('database')
                )
                self.db_name = params.get('database')
            elif db_type == "SQLite":
                self.conn = sqlite3.connect(params["database"])
            elif db_type == "PostgreSQL":
                self.conn = psycopg2.connect(
                    host=params.get('host'), user=params.get('user'),
                    password=params.get('password'), dbname=params.get('database')
                )
            
            if self.conn:
                self.cursor = self.conn.cursor()
            return "Connected", None
        except Exception as e:
            self.conn = self.cursor = None
            return None, e

    # --- NEW METHOD TO CREATE A DATABASE ---
    def create_database(self, db_type, params, db_name):
        """Connects to the server and creates a new database."""
        temp_conn = None
        try:
            if db_type == "MySQL":
                # Connect without specifying a database
                temp_conn = mysql.connector.connect(
                    host=params.get('host'),
                    user=params.get('user'),
                    password=params.get('password')
                )
                cursor = temp_conn.cursor()
                cursor.execute(f"CREATE DATABASE `{db_name}`")
            
            elif db_type == "PostgreSQL":
                # Connect to the default 'postgres' database to run CREATE DATABASE
                temp_conn = psycopg2.connect(
                    host=params.get('host'), user=params.get('user'),
                    password=params.get('password'), dbname='postgres'
                )
                temp_conn.autocommit = True # Required to run CREATE DATABASE outside a transaction block
                cursor = temp_conn.cursor()
                cursor.execute(f'CREATE DATABASE "{db_name}"')

            return f"Database '{db_name}' created.", None
        
        except Exception as e:
            return None, e
        
        finally:
            if temp_conn:
                temp_conn.close()

    def disconnect(self):
        try:
            if self.cursor: self.cursor.close()
            if self.conn: self.conn.close()
        finally:
            self.conn = self.cursor = None

    def is_connected(self):
        return self.conn and self.cursor

    def run_sql(self, query):
        if not self.is_connected():
            raise ConnectionError("Not connected to any database.")

        self.cursor.execute(query)
        low_query = query.strip().lower()

        if low_query.startswith("select"):
            rows = self.cursor.fetchall()
            cols = [d[0] for d in self.cursor.description] if self.cursor.description else []
            return rows, cols
        else:
            if hasattr(self.conn, "commit"): self.conn.commit()
            return None, None

    def fetch_tables(self):
        if not self.is_connected(): return []
        try:
            if self.db_type == "SQLite":
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            elif self.db_type == "MySQL":
                self.cursor.execute("SHOW TABLES")
            elif self.db_type == "PostgreSQL":
                q = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"
                self.cursor.execute(q)
            return [r[0] for r in self.cursor.fetchall()]
        except:
            return []

    def fetch_columns(self, table_name):
        if not self.is_connected(): return []
        try:
            if self.db_type == "SQLite":
                self.cursor.execute(f"PRAGMA table_info(`{table_name}`)")
                return [r[1] for r in self.cursor.fetchall()]
            elif self.db_type == "MySQL":
                self.cursor.execute(f"DESCRIBE `{table_name}`")
                return [r[0] for r in self.cursor.fetchall()]
            elif self.db_type == "PostgreSQL":
                q = "SELECT column_name FROM information_schema.columns WHERE table_name=%s ORDER BY ordinal_position"
                self.cursor.execute(q, (table_name,))
            return [r[0] for r in self.cursor.fetchall()]
        except:
            return []

    def fetch_table_info(self, table_name):
        if not self.is_connected():
            raise ConnectionError("Not connected to a database.")
        
        rows, headers = [], []
        if self.db_type == "MySQL":
            self.cursor.execute(f"DESCRIBE `{table_name}`")
            base_rows = self.cursor.fetchall()
            headers = ["Field", "Type", "Null", "Key", "Default", "Extra", "References"]
            
            fk_map = {}
            fk_query = """
                SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL
            """
            self.cursor.execute(fk_query, (self.db_name, table_name))
            for col, ref_table, ref_col in self.cursor.fetchall():
                fk_map[col] = f"{ref_table}({ref_col})"
            
            for row in base_rows:
                col_name = row[0]
                ref_info = fk_map.get(col_name, '')
                rows.append(list(row) + [ref_info])
                
        elif self.db_type == "SQLite":
            headers = ["ID", "Name", "Type", "Not Null", "Default Value", "PK", "References"]
            self.cursor.execute(f"PRAGMA table_info(`{table_name}`)")
            base_info = self.cursor.fetchall()
            
            fk_map = {}
            self.cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
            for row in self.cursor.fetchall():
                col_from, ref_table, ref_col = row[3], row[2], row[4]
                fk_map[col_from] = f"{ref_table}({ref_col})"

            for row in base_info:
                col_name = row[1]
                ref_info = fk_map.get(col_name, '')
                rows.append(list(row) + [ref_info])

        elif self.db_type == "PostgreSQL":
            headers = ["Column", "Data Type", "Max Length", "Is Nullable", "Default", "References"]
            fk_map = {}
            fk_query = """
                SELECT kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name=%s;
            """
            self.cursor.execute(fk_query, (table_name,))
            for col, ref_table, ref_col in self.cursor.fetchall():
                fk_map[col] = f"{ref_table}({ref_col})"

            base_query = """
                SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s ORDER BY ordinal_position;
            """
            self.cursor.execute(base_query, (table_name,))
            for row in self.cursor.fetchall():
                col_name = row[0]
                ref_info = fk_map.get(col_name, '')
                rows.append(list(row) + [ref_info])
        
        return rows, headers
