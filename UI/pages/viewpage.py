import tkinter as tk
from tkinter import ttk

from UI.pages import paging_handle


class ViewPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.main_app_body = ttk.Frame(self.master)
        self.context_action_box = self.master.master.master.master.context_action_box
        self.create_body()

    def create_body(self):
        pass

    def create_context_nav(self):
        pass

    def to_string(self):
        return f"{type(self)}"

    def on_show(self):
        self.create_context_nav()

    def on_hide(self):
        for widget in self.context_action_box.winfo_children():
            widget.destroy()

    def update(self):
        pass