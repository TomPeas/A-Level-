from tkinter import *


class Creator:
    def __init__(self, window):
        self.window = window
        self.window.title('Login')

        top_frame = LabelFrame(self.window)
        top_frame.grid(row=0, column=0)

        Label(top_frame, text='Username:').grid(row=0, column=0)
        self.name_entry = Entry(top_frame)
        self.name_entry.grid(row=0, column=1)
        name = (self.name_entry.get())

        mid_frame = LabelFrame(self.window)
        mid_frame.grid(row=2, column=0)

        Label(mid_frame, text='Password: ').grid(row=0, column=0)
        self.pass_entry = Entry(mid_frame)
        self.pass_entry.grid(row=0, column=1)
        password = (self.pass_entry.get())

        bottom_frame = LabelFrame(self.window)
        bottom_frame.grid(row=4, column=0)

        Button(bottom_frame, text = 'Login').grid(row = 0, column = 0)
        Button(bottom_frame, text = 'Quit', command = self.quit).grid(row = 0, column = 2)

    def quit(self):
        window.destroy()


if __name__ == '__main__':
    window = Tk()
    window.geometry('500x250')
    my_gui = Creator(window)
    window.mainloop()
