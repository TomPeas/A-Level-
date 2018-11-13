from tkinter import *
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
tbl_login_sql = ''' CREATE TABLE IF NOT EXISTS Login_Info(UserID text PRIMARY KEY, Username text NOT NULL, Email text NOT NULL, Password text NOT NULL)'''
insert_user_sql = ''' INSERT INTO Login_Info( UserID, Username, Email, Password) values (?,?,?,?)'''

db = Database('Santa_Login_info.db')
db.create_table(tbl_login_sql)

class NewUser:
    def __init__(self, window):
        self.window = window
        self.window.title('Create Account')

        top_frame = LabelFrame(self.window)
        top_frame.grid(row = 0, column = 0)

        Label(top_frame, text = 'Username:').grid(row = 0, column = 0)
        self.name_entry = Entry(top_frame)
        self.name_entry.grid(row = 0, column = 1)

        frame = LabelFrame(self.window)
        frame.grid(row = 2, column = 0)

        Label(frame, text = 'Email:        ').grid(row = 0, column = 0)
        self.email_entry = Entry(frame)
        self.email_entry.grid(row = 0, column = 1)

        mid_frame = LabelFrame(self.window)
        mid_frame.grid(row = 4, column = 0)

        Label(mid_frame, text = 'Password: ').grid(row = 0, column = 0)
        self.pass_entry = Entry(mid_frame)
        self.pass_entry.grid(row = 0, column = 1)

        bottom_frame = LabelFrame(self.window)
        bottom_frame.grid(row = 6, column = 0)

        Button(bottom_frame, text = 'Create', command = self.create).grid(row = 0, column = 0)
        Button(bottom_frame, text = 'Quit', command = self.quit).grid(row = 0, column = 2)

    def create(self):
        with open('cur_user_id.txt', 'r') as data:
            userid = data.read()
        name = (self.name_entry.get())
        email = (self.email_entry.get())
        password = (self.pass_entry.get())
        data = (userid, name, email, password)
        db.update_table(insert_user_sql, data)
        with open('cur_user_id.txt', 'w') as data:
            userid = int(userid) + 1
            userid = str(userid)
            data.write(userid)

    def quit(self):
        window.destroy()

if __name__ == '__main__':
    window = Tk()
    window.geometry('200x100')
    newuser = NewUser(window)
    window.mainloop()