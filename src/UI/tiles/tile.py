import tkinter as tk

import src.UI.pages.paging_handle as PagingHandle
from src.UI.pages.paging_handle import PagesEnum
from src.structures.records.requirement import Requirement


class Tile(tk.Frame):
    default_width = 25
    default_height = 300

    def __init__(self, master, data, **kwargs):
        super().__init__(master, bd=1, relief=tk.SOLID, **kwargs)
        self.dragging = False
        self.selected = False
        self.data = data
        self.create_widgets()
        self.bind_child_events()
        self.clone = None

    def create_widgets(self):
        raise NotImplementedError("Subclasses should implement this!")

    def update_widgets(self):
        raise NotImplementedError("Subclasses should implement this!")

    def bind_child_events(self):
        # Bind events to the tile itself
        self.bind("<Button-1>", self.on_click_start)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<Double-Button-1>", self.on_double_click)

        # Bind events to all child widgets
        for child in self.winfo_children():
            child.bind("<Button-1>", self.on_click_start, add='+')
            child.bind("<B1-Motion>", self.on_drag, add='+')
            child.bind("<ButtonRelease-1>", self.on_release, add='+')
            child.bind("<Double-Button-1>", self.on_double_click, add='+')

            child.propagate(False)


    def on_click_start(self, event):
        # Initialize last mouse position
        self.last_x = event.x
        self.last_y = event.y
        if self.clone is None:
            self.create_clone()
        self.clone.lift()
        print(f"Tile clicked: {self.data}")

    def on_drag(self, event):
        # Calculate the new position
        # Calculate the movement since the last drag event
        dx = event.x - self.last_x
        dy = event.y - self.last_y

        # Calculate the new position
        if self.clone:
            x = self.clone.winfo_x() + dx
            y = self.clone.winfo_y() + dy
            self.clone.place(x=x, y=y)

            # Update last mouse position
            self.last_x = event.x
            self.last_y = event.y
            print(f"x:{x}, y:{y}")

    def on_release(self, event):
        # Destroy the clone and reset the reference
        if self.clone:
            self.master.update_idletasks()
            x, y = event.x_root, event.y_root  # Event coordinates
            target = self.find_tile_under_coordinates(x, y)
            if isinstance(target, Tile) and target != self:
                print(f"{self.data} dropped on {target.data}")
                #connect(self.data, target.data)  # Call connect function
            self.clone.destroy()
            self.clone = None

    def create_clone(self):
        # Create a clone of the tile
        self.clone = tk.Frame(self.master, bg='white', highlightbackground="black", highlightthickness=1)
        for child in self.winfo_children():
            text = child.cget("text")
            new_child = tk.Label(self.clone, text=text)
            new_child.pack(fill=tk.BOTH, expand=True)
        self.clone.place(x=self.winfo_x(), y=self.winfo_y(), width=self.winfo_width(), height=self.winfo_height())

    def find_tile_under_coordinates(self, x, y):
        for widget in self.master.winfo_children():
            if isinstance(widget, Tile) and self.is_within_widget(widget, x, y):
                return widget
        return None

    def is_within_widget(self, widget, x, y):
        x0, y0, x1, y1 = widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_rootx() + widget.winfo_width(), widget.winfo_rooty() + widget.winfo_height()
        return x0 <= x <= x1 and y0 <= y <= y1

    def get_data(self):
        return self.data

    def on_double_click(self, event):
        print(f"{self.data} double clicked")
        self.deselect()
        if isinstance(self.data, Requirement):
            PagingHandle.get_page(PagesEnum.REQUIREMENT_EXTENDED).requirement = self.data
            PagingHandle.show_page(PagesEnum.REQUIREMENT_EXTENDED)

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