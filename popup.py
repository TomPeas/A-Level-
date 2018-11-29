from tkinter import *

class popup:
    def __init__(self, window, msg):
        self.window = window
        self.window.title("Error")
        popup = LabelFrame(self.window)
        popup.grid(row = 0, column = 0)
        Label(popup, text = msg).grid(row = 0, column = 0)
        Button(popup, text = 'Ok', command = lambda: self.window.destroy()).grid(row = 1, column = 0)