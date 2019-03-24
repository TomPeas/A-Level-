import hashlib
import uuid
from tkinter import *
from tkinter import ttk
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
                page4.geometry('1000x500')
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

#        self.tree = ttk.Treeview(display_frame)
#        self.tree['columns'] = ('dishes','prices', 'section')
#        self.tree.column('dishes', width = 500)
#        self.tree.column('prices', width = 100)
#        self.tree.column('section', width = 100)
#        self.tree.heading('dishes', text = 'Dish')
#        self.tree.heading('prices', text = 'Price')
#        self.tree.heading('section', text = 'Section')
#        self.tree.grid(row = 1, column = 1)
#        self.all_items(self.tree)

        box = Tk()
        sb = Scrollbar(box, orient = 'vertical')
        order = Listbox(box, width=75, height=20, yscrollcommand=sb.set)
        sb.config(command = order.yview)
        sb.pack(side = 'right', fill = 'y')
        self.order = order
        order.pack(side = 'left', fill = 'both', expand = True )

        Button(option_frame, text = 'All', command = lambda: self.all_items(display_frame, order)).grid(row = 0, column = 0)
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

    def all_items(self, display_frame, order):
        items_to_display = mdb.find_all()
        print(len(items_to_display))
        page2_frame = LabelFrame(self.window)
        page2_frame.grid(row = 0, column = 1)
        page3_frame = LabelFrame(self.window)
        page3_frame.grid(row = 0, column = 1)
        r=0
        j=0
        x=0
        k=0
        m=0
        def menu_page_1(r):
            page2_frame.grid_remove()
            page3_frame.grid_remove()
            display_frame.grid(row = 0, column = 1)
            for i in range(41):
                if i < 26:
                    Button(display_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=i, column=0)
                elif i < 42:
                    Button(display_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=r, column=2)
                    r+=1
        def menu_page_2(j, x):
            display_frame.grid_remove()
            page3_frame.grid_remove()
            page2_frame.grid(row = 0, column = 1)
            for i in range(42, 83):
                if i < 68:
                    Button(page2_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=j, column=0)
                    j+=1
                elif i < 84:
                    Button(page2_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=x, column=2)
                    x+=1
            Button(page2_frame, text = ' Back', command = lambda : menu_page_1(r)).grid(row = 4, column = 3)
            Button(page2_frame, text = 'Next', command = lambda : menu_page_3(m,k)).grid(row = 3, column = 3)
        def menu_page_3(m,k):
            page2_frame.grid_remove()
            display_frame.grid_remove()
            page3_frame.grid(row = 0, column = 1)
            for i in range(84, 124):
                if i < 110:
                    Button(page3_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=m, column=0)
                    m+=1
                if i < 125:
                    Button(page3_frame, text=items_to_display[i],command=lambda i=i: add_to_listbox(items_to_display[i], order, i)).grid(row=k, column=2)
                    k+=1
            Button(page3_frame, text = 'Back', command = lambda : menu_page_2(j,x)).grid(row = 3, column = 3)
        menu_page_1(r)
        Button(display_frame, text='Next', command= lambda: menu_page_2(j, x)).grid(row = 3, column = 3)

def add_to_listbox(data, order, i):
    split_data = data[0]
    print(split_data)
    price = mdb.find_price(mdb.find_menu_price_id((mdb.find_dish_id(split_data))[0][0])[0][0])[0][0]
    print(price)
    order.insert(i, split_data, price)
    order.pack()



page1 = Tk()
page1.iconbitmap('san_icon.ico') # adds logo to top right corner
page1.geometry('300x120')
Base(page1)
page1.mainloop()
