import tkinter as tk
from tkinter import ttk


class ComboboxWithAdd(tk.Frame):
    def __init__(self, master, options=None, selected_callback=None):
        super().__init__(master)

        self.options = options if options else []

        self.variable = tk.StringVar(self)
        self.variable.set('')
        self.combobox = ttk.Combobox(self, textvariable=self.variable, values=self.options)
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if self.options:
            self.combobox['values'] = self.options

        if selected_callback:
            self.combobox.bind("<<ComboboxSelected>>", selected_callback)

    def set_values(self, values):
        self.combobox['values'] = values

    def update(self, options=None):
        # Add blank value at the top
        values_with_blank = [''] + options if options else ['']
        self.set_values(values_with_blank)
        # Set selected value to the top one
        self.variable.set(values_with_blank[0])

    def clear(self):
        # Add blank value at the top
        values_with_blank = [''] + self.options if self.options else ['']
        self.set_values(values_with_blank)
        # Set selected value to the top one
        self.variable.set(values_with_blank[0])

    def set_options(self, options):
        self.options = options
        self.update(options)
