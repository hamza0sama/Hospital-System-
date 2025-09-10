import pyodbc
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connection(self):
        try:
            print("Starting connection...")
            server = 'HamzaOsama'
            database = 'Hospital'

            self.conn = pyodbc.connect(
                f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                f'SERVER={server};'
                f'DATABASE={database};'
                f'Trusted_Connection=yes;'
            )
            print("Connection successful")

        except Exception as e:
            print("Error in connection:", e)

    def close_Connection(self):
        try:
            if self.conn:
                self.conn.close()
                print("Connection closed")
        except Exception as e:
            print("Error in closing connection:", e)

    def get_cursor(self):
        if self.conn:
            self.cursor = self.conn.cursor()
            return self.cursor
        else:
            print("No active connection to get cursor from.")
            return None

    def close_cursor(self):
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
                print("Cursor closed")
        except Exception as e:
            print("Error closing cursor:", e)

    def commit(self):
        if self.conn:
            self.conn.commit()
        else:
            print("No active connection to commit.")

    def insert(self, table, cols, data):
        try:
            cursor = self.get_cursor()
            placeholders = ", ".join(["?"] * len(data))
            query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
            cursor.execute(query, data)
            self.commit()
            print("Done")
        except Exception as e:
            if "PRIMARY KEY" in str(e) or "UNIQUE" in str(e):
                print(f"Id={data[0]} is not available")
            else:
                print(e)
        finally:
            self.close_cursor()

    def update(self, table, cols, updated_data, ID):
        try:
            if  self.search_id(table, ID) is not None:
                cursor = self.get_cursor()
                set_clause = ", ".join([f"{col} = ?" for col in cols])
                query = f"UPDATE {table} SET {set_clause} WHERE {table}_id = ?"
                cursor.execute(query, (*updated_data, ID))
                self.commit()
                print("Updated successfully")
            else:
                print(f"The id:{ID} does not exist")
        finally:
            self.close_cursor()

    def delete(self, table, ID):
        try:
            cursor = self.get_cursor()
            query = f"DELETE FROM {table} WHERE {table}_id=?"
            cursor.execute(query, (ID,))
            self.commit()
            print(f"Deleted id={ID} from {table}")
        finally:
            self.close_cursor()

    def display(self, table):
        try:
            cursor = self.get_cursor()
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        finally:
            self.close_cursor()

    def search_id(self, table, ID):
        try:
            cursor = self.get_cursor()
            query = f"SELECT * FROM {table} WHERE {table}_id=?"
            cursor.execute(query, (ID,))
            row = cursor.fetchone()
            if row:
                print("Found!")
                return row
            else:
                print("Not found!")
                return None
        finally:
            self.close_cursor()

    def search_name(self, table, name):
        try:
            cursor = self.get_cursor()
            query = f"SELECT * FROM {table} WHERE {table}_name=?"
            cursor.execute(query, (name,))
            row = cursor.fetchall()
            if row:
                print("Found!")
                return row
            else:
                print("Can't find!")
                return None
        finally:
            self.close_cursor()

    def get_last_id(self, table, id_column):
        try:
            cursor = self.get_cursor()
            query = f"SELECT TOP 1 {id_column} FROM {table} ORDER BY {id_column} DESC"
            cursor.execute(query)
            row = cursor.fetchone()
            return row[0] if row else None
        finally:
            self.close_cursor()
