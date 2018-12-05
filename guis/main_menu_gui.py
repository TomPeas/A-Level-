from tkinter import *
from login_gui import UserLogin
from new_user_gui import NewUser

class Menu:
    def __init__(self, window):
        self.window = window
        self.window.title('Start Menu')

        top_frame = LabelFrame(self.window)
        top_frame.grid(row = 0, column = 0)

        Button(top_frame, text = 'Create Account', command = self.new_user).grid( row = 0, column = 0)
        Button(top_frame, text = 'Login', command = self.login_window).grid( row = 1, column = 0)
        Button(top_frame, text = 'Quit', command = self.window.destroy).grid( row = 3, column = 0)

    def new_user(self):
        page2 = Tk()
        page2.geometry('500x500')
        NewUser(page2)

    def login_window(self):
        page3 = Tk()
        page3.geometry('500x500')
        UserLogin(page3)