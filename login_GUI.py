from tkinter import *

class UserLogin:
    def __init__(self, window):
        self.window = window
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
        Button(bottom_frame, text = 'Quit', command = lambda: self.window.destroy).grid(row = 0, column = 2)

    def login(self, window):
        username = (self.username.get())
        user_password = (self.password.get())
        stored_password = db.find_password(username,)
        print(stored_password)
        if user_password == stored_password:
            # open next window
            window.destroy()