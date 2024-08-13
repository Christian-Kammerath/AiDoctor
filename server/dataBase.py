import os.path
import sqlite3


class DataBase:
    def __init__(self, data_base_name):
        self.connection = sqlite3.connect(data_base_name + '.db')

    # closes the contact to the database
    def commit_and_close(self, cursor):
        self.connection.commit()
        cursor.close()

    # creates new table as long as it does not already exist
    def create_table(self, table_name, value):
        try:
            value = ", ".join(value)  # Konvertiere die Tupel in eine durch Komma getrennte Zeichenkette
            cursor = self.connection.cursor()
            create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({value})'
            cursor.execute(create_table_query)
            self.commit_and_close(cursor)
            return f"{table_name} was created"
        except Exception as e:
            return str(e)

    # Insert values into the table
    def insert(self, table_name, columns="", *value):
        try:
            cursor = self.connection.cursor()
            placeholders = ", ".join(["?"] * len(value))
            if len(columns) == 0:
                insert_query = f'INSERT INTO {table_name} VALUES ({placeholders})'
            else:
                insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

            cursor.execute(insert_query, value)
            last_id = cursor.lastrowid
            self.commit_and_close(cursor)

            if last_id is not None:
                return last_id
            else:
                return "No ID available. Value was entered."
        except Exception as e:
            return str(e)

    # returns entire table
    def get_all_table_values(self, table_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            result = cursor.fetchall()
            self.commit_and_close(cursor)
            return result
        except Exception as e:
            return e

    # allow to select an entry from a database
    def select(self, from_table, what, where, params):
        try:
            cursor = self.connection.cursor()
            query = f'SELECT {what} FROM {from_table} WHERE {where}'
            cursor.execute(query, params)
            result = cursor.fetchall()
            self.commit_and_close(cursor)
            return result
        except Exception as e:
            raise e


    # enables an individual query to be sent to the database
    def individual_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            self.commit_and_close(cursor)
            return result
        except Exception as e:
            return e
