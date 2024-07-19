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
            cursor = self.connection.cursor()
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({value})')
            self.commit_and_close(cursor)
            return f"{table_name} was created"
        except Exception as e:
            return e

    # Insert values into the table
    def insert(self, table_name, value):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'INSERT INTO {table_name} VALUES {value}')
            self.commit_and_close(cursor)
            return f"INSERT successful"
        except Exception as e:
            return e

    # returns entire table
    def get_table(self, table_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f'SELECT * FROM {table_name}')
            result = cursor.fetchall()
            self.commit_and_close(cursor)
            return result
        except Exception as e:
            return e

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
