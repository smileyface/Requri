import tkinter as tk


class ViewPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

    def to_string(self):
        return f"{type(self)}"