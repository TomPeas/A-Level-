import tkinter as tk

class ScrolledWindow(tk.Frame):
    def __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas
        use "Instance".scrollwindow
       """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.canv_w = canv_w
        self.canv_h = canv_h

        # creating a scrollbars
        self.yscrlbr = tk.Scrollbar(self.parent)
        self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')
        # creating a canvas
        self.canv = tk.Canvas(self.parent)
        self.canv.config(relief = 'flat', width = self.canv_w, heigh = self.canv_h, bd = 2)
        # placing a canvas into frame
        self.canv.grid(column = 0, row = 0, sticky = 'nsew')
        # accociating scrollbar comands to canvas scroling
        self.yscrlbr.config(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = tk.Frame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, self.canv_w, self.canv_h)) #xscrollcommand = self.xscrlbr.set,


        self.scrollwindow.bind('<Configure>', self._configure_window)
        return

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)