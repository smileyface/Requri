import tkinter as tk

from UI.pages.paging_handle import get_page, show_page, PagesEnum
from structures.connector import connect
from structures.records.requirement import Requirement


class Tile(tk.Frame):
    default_width = 25
    default_height = 300

    def __init__(self, master, data, **kwargs):
        super().__init__(master, bd=1, relief=tk.SOLID, **kwargs)
        self.dragging = False
        self.selected = False
        self.data = data
        self.config(width=self.default_width, height=self.default_height)  # Set default width and height
        self.bind_events()

    def bind_events(self):
        self.bind("<Button-1>", self.on_click)
        self.bind("<Button1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Double-1>", self.on_double_click)

    def bind_child_events(self):
        for child in self.winfo_children():
            child.bind("<Button-1>", self.on_child_click)
            child.bind("<Button1-Motion>", self.on_drag)
            child.bind("<ButtonRelease-1>", self.on_release)
            child.bind("<Double-1>", self.on_child_double_click)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.clicked = True  # Flag to indicate click
        self.after(100, self.check_drag)  # Check for drag after 100ms

    def on_release(self, event):
        self.clicked = False
        if self.dragging:
            self.dragging = False
            self.on_drop(event)

    def on_child_click(self, event):
        # Handle click event for child components
        print("Child clicked")
        self.start_x = self.winfo_x()
        self.start_y = self.winfo_y()
        self.clicked = True
        self.after(100, self.check_drag)

    def on_child_double_click(self, event):
        print(f"{self.data} double clicked")
        self.deselect()
        if isinstance(self.data, Requirement):
            get_page(PagesEnum.REQUIREMENT_EXTENDED).requirement = self.data
            show_page(PagesEnum.REQUIREMENT_EXTENDED)

    def check_drag(self):
        if not self.clicked:
            print("It's clicked")
            self.toggle_selection()  # If not dragged, select the tile
        else:
            print("It's drugged")
            self.clone = self.clone_tile()
            self.dragging = True

    def on_drag(self, event):
        x = self.winfo_x() + event.x - self.start_x
        y = self.winfo_y() + event.y - self.start_y
        self.clone.place(x=x, y=y)

    def on_drop(self, event):
        self.clone.place_forget()  # Remove clone
        self.master.update_idletasks()
        x, y = event.x_root, event.y_root  # Event coordinates
        target = self.find_tile_under_coordinates(x, y)
        if isinstance(target, Tile) and target != self:
            print(f"{self.data} dropped on {target.data}")
            connect(self.data, target.data)  # Call connect function

    def find_tile_under_coordinates(self, x, y):
        for widget in self.master.winfo_children():
            if isinstance(widget, Tile) and self.is_within_widget(widget, x, y):
                return widget
        return None

    def is_within_widget(self, widget, x, y):
        x0, y0, x1, y1 = widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height()
        return x0 <= x <= x1 and y0 <= y <= y1

    def clone_tile(self):
        clone = Tile(self.master, self.data)
        clone.configure(background="gray")  # Set background color to gray
        clone.place(in_=self.master, x=self.winfo_x(), y=self.winfo_y())  # Place at current position
        return clone

    def get_data(self):
        return self.data

    def on_double_click(self, event):
        print(f"{self.data} double clicked")
        self.deselect()
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

    def update(self):
        pass