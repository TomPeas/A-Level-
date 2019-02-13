import hashlib
import uuid
from tkinter import *
from popup import Popup, Lockup
from database_base import Database
from guis import scrollwheel
from PIL import Image, ImageTk

# creates the database to store user information
tbl_login_sql = ''' CREATE TABLE IF NOT EXISTS Login_Info(UserID text PRIMARY KEY, Username text NOT NULL, Email text NOT NULL, Password text NOT NULL)'''
insert_user_sql = ''' INSERT INTO Login_Info( UserID, Username, Email, Password) values (?,?,?,?)'''
db = Database('Santa_Login_info.db')
db.create_table(tbl_login_sql)

# initialised the database that stores the menu items
mdb = Database('Santa_Database.db')

# hashes a generated password
def hash_password(password):
    num = uuid.uuid4().hex
    return hashlib.sha256(num.encode() + password.encode()).hexdigest() + ':' + num

# checks the hash password against the user entered password, returns true if they are the same
def check_password(hashed_password, user_password):
    password, num = hashed_password.split(':')
    return password == hashlib.sha256(num.encode() + user_password.encode()).hexdigest()


class Base: # the base window, stays open as if closed the program closes
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
        self.window.title('Start Menu')

        image_frame = LabelFrame(self.window)
        image_frame.place(x = 200, y = 25)
        logo = PhotoImage(file = "C:\\Users\\Tom\\.PyCharmCE2016.3\\Project\\A-Level_CS\\san.gif")
        Label(image_frame, image = logo).grid(row = 0, column = 0)

        top_frame = LabelFrame(self.window)
        top_frame.place(x = 14, y = 15)

        Button(top_frame, text = 'Create Account', command = self.new_user).grid( row = 0, column = 0)
        Button(top_frame, text = 'Login', command = self.login_window).grid( row = 1, column = 0)
        Button(top_frame, text = 'Quit', command = self.window.destroy).grid( row = 3, column = 0)

    @staticmethod
    def new_user(): # opens the new user window
        page2 = Tk()
        page2.geometry('300x100')
        NewUser(page2)

    @staticmethod
    def login_window(): # opens the login window
        page3 = Tk()
        page3.geometry('500x500')
        UserLogin(page3)


class UserLogin: # window for the user login
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
        self.window.title('Login')
        self.login_attempts = 0

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
        msg = 'Incorrect Username or Password!'
        username = (self.username.get())
        found = db.find_username(username)
        if found:
            user_password = "('"+ str((self.password.get())) + "',)" # When the password is read from the database it is in this format
            stored_password = db.find_password(username,) # returns in list with format "('password',)", at pos 0 in list, use as string for comparison
            if user_password == str(stored_password[0]):
                page4 = Tk()
                page4.geometry('500x500')
                MainMenu(page4)
                window.destroy()
            elif user_password != str(stored_password[0]) and self.login_attempts < 3:
                box = Tk()
                Popup(box, msg)
                self.login_attempts += 1
            elif user_password != str(stored_password[0]) and self.login_attempts >= 3:
                box = Tk()
                Lockup(box, msg)
                self.login_attempts = 0
        elif not found and self.login_attempts < 3:
            box = Tk()
            Popup(box, msg)
            self.login_attempts += 1
        elif not found and self.login_attempts >= 3:
            box = Tk()
            Lockup(box, msg)
            self.login_attempts = 0

class NewUser: # window for creating a new user account
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


class MainMenu: # main window, displays the items that can be ordered and allows the user to create an order (when it works)
    def __init__(self, window):
        self.window = window
        self.window.configure(background = '#808080')
        self.window.title('Main Menu')

        option_frame = LabelFrame(self.window)
        option_frame.grid(row = 0, column = 0)

       # sb1 = Scrollbar(self.window, orient='vertical')
        display_frame = LabelFrame(self.window)
       # sb1.config(command = self.window.yview)
       # sb1.pack(side = 'right', fill = 'y')
        display_frame.grid(row = 0, column = 1)

        box = Tk()
        sb = Scrollbar(box, orient = 'vertical')
        order = Listbox(box, width=50, height=20, yscrollcommand=sb.set)
        sb.config(command = order.yview)
        sb.pack(side = 'right', fill = 'y')
        self.order = order
        order.pack(side = 'left', fill = 'both', expand = True )

        Button(option_frame, text = 'All', command = lambda: self.all_items(display_frame, order )).grid(row = 0, column = 0)
        Button(option_frame, text = 'Starters', command = self.window.destroy).grid(row = 1, column = 0)
        Button(option_frame, text = 'Soups', command = self.window.destroy).grid(row = 2, column = 0)
        Button(option_frame, text = 'Poultry Dishes', command = self.window.destroy).grid(row = 3, column = 0)
        Button(option_frame, text = 'Beef Dishes', command = self.window.destroy).grid(row = 4, column = 0)
        Button(option_frame, text = 'Pork and Lamb Dishes', command = self.window.destroy).grid(row = 5, column = 0)
        Button(option_frame, text = 'Curry Dishes', command = self.window.destroy).grid(row = 6, column = 0)
        Button(option_frame, text = 'Seafood Dishes', command = self.window.destroy).grid(row = 7, column = 0)
        Button(option_frame, text = 'Vegetarian Dishes', command = self.window.destroy).grid(row = 8, column = 0)
        Button(option_frame, text = 'Nice and Noodle Dishes', command = self.window.destroy).grid(row = 9, column = 0)
        Button(option_frame, text = 'Extras', command = self.window.destroy).grid(row = 10, column = 0)

    @staticmethod
    def all_items(display_frame, order):
        items_to_display = mdb.find_all()
        for i in range(len(items_to_display)):
            Button(display_frame, text = items_to_display[i],command = lambda i=i : add_to_listbox(items_to_display[i], order, i)).grid(row = i, column = 0)

def add_to_listbox(data, order, i):
    price = mdb.find_pt('Price', 'PriceID', str(mdb.find_mt('PriceID', 'DishID', str(mdb.find_dt('DishID', 'Dish', str(data))))))
    item = (str(i) + '.' + ' ' + str(data))
    order.insert(i, item)
    order.pack()




page1 = Tk()
page1.iconbitmap('san_icon.ico') # adds logo to top right corner
page1.geometry('300x120')
Base(page1)
page1.mainloop()