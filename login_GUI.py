from tkinter import *
import sqlite3
import hashlib
import uuid

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

# hashes a generated password
def hash_password(password):
    num = uuid.uuid4().hex
    return hashlib.sha256(num.encode() + password.encode()).hexdigest() + ':' + num

def check_password(hashed_password, user_password):
    password, num = hashed_password.split(':')
    return password == hashlib.sha256(num.encode() + user_password.encode()).hexdigest()

class Menu:
    def __init__(self, window):
        self.window = window
        self.window.title('Start Menu')

        top_frame = LabelFrame(self.window)
        top_frame.grid(row = 0, column = 0)

        Button(top_frame, text = 'Create Account', command = self.open_create).grid( row = 3, column = 0)

    def open_create(self):
        page2 = Tk()
        page2.geometry('500x500')
        NewUser(page2)

    def quit(self, window):
        window.destroy()


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

        Button(bottom_frame, text = 'Create', command = lambda: self.create(window)).grid(row = 0, column = 0)
        Button(bottom_frame, text = 'Quit', command = lambda: self.quit(window)).grid(row = 0, column = 2)

    def create(self,window):
        with open('cur_user_id.txt', 'r') as data:
            userid = data.read()
        name = (self.name_entry.get())
        email = (self.email_entry.get())
        password = hash_password(self.pass_entry.get())
        data = (userid, name, email, password)
        db.update_table(insert_user_sql, data)
        with open('cur_user_id.txt', 'w') as data:
            userid = int(userid) + 1
            userid = str(userid)
            data.write(userid)
        window.destroy()


    def quit(self, window):
        window.destroy()

page1 = Tk()
page1.geometry('500x500')
Menu(page1)
page1.mainloop()
