import tkinter as tk
from tkinter import ttk


class ComboboxWithAdd(tk.Frame):
    def __init__(self, master, options=None, selected_callback=None):
        super().__init__(master)

        self.options = options if options else []

        self.variable = tk.StringVar(self)
        self.combobox = ttk.Combobox(self, textvariable=self.variable, values=self.options)
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if self.options:
            self.combobox['values'] = self.options

        if selected_callback:
            self.combobox.bind("<<ComboboxSelected>>", selected_callback)

    def set_values(self, values):
        self.options = values
        self.combobox['values'] = self.options
