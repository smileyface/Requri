import tkinter as tk
from tkinter import ttk
from typing import List, Callable, Optional


class ComboboxWithAdd(tk.Frame):
    def __init__(self, master, options: Optional[List[str]] = None, selected_callback: Optional[Callable] = None):
        super().__init__(master)
        self.options = options if options else []
        self.selected_callback = selected_callback

        self.variable = tk.StringVar(self)
        self.variable.set('')

        self.combobox = ttk.Combobox(self, textvariable=self.variable, values=self.options)
        self.combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        if self.selected_callback:
            self.combobox.bind("<<ComboboxSelected>>", self.selected_callback)

    def set_values(self, values: List[str]):
        """
        Set the values for the combobox.
        """
        self.combobox['values'] = values

    def update(self, options: Optional[List[str]] = None):
        """
        Update the combobox with new options, adding a blank value at the top.
        """
        if options is not None:
            self.options = options
        else:
            self.options = []
        values_with_blank = [''] + self.options
        self.set_values(values_with_blank)
        self.variable.set(values_with_blank[0])

    def clear(self):
        """
        Clear the combobox, resetting to include only the initial options with a blank value at the top.
        """
        self.update(self.options)

    def set_options(self, options: List[str]):
        """
        Set new options for the combobox.
        """
        self.options = options
        self.update()

    def configure(self, **kwargs):
        """
        Configure the combobox. Supports updating values and the selected callback.
        """
        if 'values' in kwargs:
            self.set_options(kwargs['values'])
        if 'selected_callback' in kwargs:
            if self.selected_callback:
                self.combobox.unbind("<<ComboboxSelected>>", self.selected_callback)
            self.selected_callback = kwargs['selected_callback']
            self.combobox.bind("<<ComboboxSelected>>", self.selected_callback)
        super().configure(**kwargs)
