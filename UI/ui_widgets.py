import tkinter as tk

class Label(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class Entry(tk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class Button(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class Listbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)