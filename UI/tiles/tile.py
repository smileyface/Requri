import tkinter as tk

from UI.pages.paging_handle import get_page, show_page, PagesEnum
from structures.requirement import Requirement


class Tile(tk.Frame):
    default_width = 25
    default_height = 300

    def __init__(self, master, data, **kwargs):
        super().__init__(master, bd=1, relief=tk.SOLID, **kwargs)
        self.selected = False
        self.data = data
        self.config(width=self.default_width, height=self.default_height)  # Set default width and height
        self.bind_events()

    def bind_events(self):
        self.bind("<Button-1>", self.on_click)
        self.bind_child_events()

    def bind_child_events(self):
        for child in self.winfo_children():
            child.bind("<Button-1>", self.on_child_click)

    def on_click(self, event):
        print("Clicked")
        self.toggle_selection()

    def on_child_click(self, event):
        # Handle click event for child components
        print("Child clicked")
        self.toggle_selection()

    def get_data(self):
        return self.data

    def on_double_click(self, event):
        if isinstance(self.data, Requirement):
            get_page(PagesEnum.REQUIREMENT_EXTENDED).requirement = self.data
            show_page(PagesEnum.REQUIREMENT_EXTENDED)

    def toggle_selection(self):
        if not self.selected:
            self.select()
        else:
            self.deselect()

    def select(self):
        self.selected = True
        self.config(borderwidth=2, relief=tk.SOLID, highlightbackground="blue")

    def deselect(self):
        self.selected = False
        self.config(borderwidth=1, relief=tk.SOLID)