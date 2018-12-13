from tkinter import *
import time

class Popup:
    def __init__(self, window, msg):
        self.window = window
        self.window.title("Error")
        popup = LabelFrame(self.window)
        popup.grid(row = 0, column = 0)
        Label(popup, text = msg).grid(row = 0, column = 0)
        Button(popup, text = 'Ok', command = lambda: self.window.destroy()).grid(row = 1, column = 0)

class Lockup:
    def __init__(self, window, msg):
        self.window = window
        self.window.title("Locked")
        count = 30
        popup = LabelFrame(self.window)
        popup.grid(row = 0, column = 0)
        Label(popup, text = msg).grid(row = 0, column = 0)
        while count != 0:
            Label(popup, text = 'Too many failed logins! Account locked for %s seconds' % count).grid(row = 1, column = 0)
            count -= 1
            time.sleep(1)
        if count == 0:
            Button(popup, text = 'Ok', command = lambda: self.window.destroy()).grid(row = 3, column = 0)


