import sqlite3

class Database:
    def __init__(self, db_name):
        with sqlite3.connect(db_name) as self.connect:
            self.cursor = self.connect.cursor()
            self.connect.execute('PRAGMA foreign_keys = on')

    def create_table(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def update_table(self, sql, data):
        self.cursor.execute(sql, data)
        self.connect.commit()

    def find_password(self, data):
        self.cursor.execute(''' SELECT Password FROM Login_Info WHERE Username = ? ''', (data,))
        stored_pass = self.cursor.fetchall()
        return stored_pass

    def find_username(self, data):
        s_data = "('" + str(data) + "',)"  # When the the username is read from the database it is in this format
        self.cursor.execute(''' SELECT Username FROM Login_Info ''')
        stored_usernames = [str(each) for each in self.cursor.fetchall()]
        if s_data in stored_usernames:
            return True
        return False