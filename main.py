import hashlib
import uuid
from tkinter import *
from popup import popup
from database_base import Database

tbl_login_sql = ''' CREATE TABLE IF NOT EXISTS Login_Info(UserID text PRIMARY KEY, Username text NOT NULL, Email text NOT NULL, Password text NOT NULL)'''
insert_user_sql = ''' INSERT INTO Login_Info( UserID, Username, Email, Password) values (?,?,?,?)'''
db = Database('Santa_Login_info.db')
db.create_table(tbl_login_sql)

# hashes a generated password
def hash_password(password):
    num = uuid.uuid4().hex
    return hashlib.sha256(num.encode() + password.encode()).hexdigest() + ':' + num

# checks the hash password against the user entered password, returns true if they are the same
def check_password(hashed_password, user_password):
    password, num = hashed_password.split(':')
    return password == hashlib.sha256(num.encode() + user_password.encode()).hexdigest()

class UserLogin:
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
        self.window.title('Login')

        top_frame = LabelFrame(self.window)
        top_frame.grid(row = 0, column = 0)

        Label(top_frame, text = 'Username:').grid(row = 0, column = 0)
        self.username = Entry(top_frame)
        self.username.grid(row = 0, column = 1)

        Label(top_frame, text = 'Password:').grid(row = 1, column = 0)
        self.password = Entry(top_frame)
        self.password.grid(row = 1, column = 1)

        bottom_frame = LabelFrame(self.window)
        bottom_frame.grid(row = 1, column = 0)

        Button(bottom_frame, text = 'Login', command = lambda: self.login(window)).grid(row = 0, column = 0)
        Button(bottom_frame, text = 'Quit', command = lambda: self.window.destroy()).grid(row = 0, column = 2)

    def login(self, window):
        username = (self.username.get())
        user_password = "('"+ str((self.password.get())) + "',)" # When the password is read from the database it is in this format
        stored_password = db.find_password(username,) # returns in list with format "('password',)", at pos 0 in list, use as string for comparison
        if user_password == str(stored_password[0]):

            window.destroy()
        else:
            box = Tk()
            popup(box, 'Incorrect Username or Password!')

class Menu:
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
        self.window.title('Start Menu')

        image_frame = LabelFrame(self.window)
        image_frame.place(x = 10, y = 5)
        self.img = PhotoImage(file = 'san.png')

        top_frame = LabelFrame(self.window)
        top_frame.place(x = 14, y = 15)

        Button(top_frame, text = 'Create Account', command = self.new_user).grid( row = 0, column = 0)
        Button(top_frame, text = 'Login', command = self.login_window).grid( row = 1, column = 0)
        Button(top_frame, text = 'Quit', command = self.window.destroy).grid( row = 3, column = 0)

    @staticmethod
    def new_user():
        page2 = Tk()
        page2.geometry('300x100')
        NewUser(page2)

    @staticmethod
    def login_window():
        page3 = Tk()
        page3.geometry('500x500')
        UserLogin(page3)


class NewUser:
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
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
        Button(bottom_frame, text = 'Quit', command = self.window.destroy).grid(row = 0, column = 2)

    def create(self,window):
        with open('cur_user_id.txt', 'r') as data:
            userid = data.read()
        name = (self.name_entry.get())
        email = (self.email_entry.get())
        password = self.pass_entry.get()
        data = (userid, name, email, password)
        db.update_table(insert_user_sql, data)
        with open('cur_user_id.txt', 'w') as data:
            userid = int(userid) + 1
            userid = str(userid)
            data.write(userid)
        window.destroy()


page1 = Tk()
page1.geometry('50x120')
Menu(page1)
page1.mainloop()