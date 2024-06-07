import tkinter as tk
from tkinter import ttk
import logging

class Traceablilty_Edit_Tab(tk.Frame):
    def __init__(self, tab):
        self.connectable_listbox = ttk.Treeview(tab)
        self.connected_listbox = ttk.Treeview(tab)

        self.connectable_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.connected_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.connectable_listbox.bind('<<TreeviewSelect>>', self.on_select)
        self.connectable_listbox.bind('<B1-Motion>', self.on_drag)
        self.connectable_listbox.bind('<ButtonRelease-1>', self.on_drop)

        self.connected_listbox.bind('<<TreeviewSelect>>', self.on_select)
        self.connected_listbox.bind('<B1-Motion>', self.on_drag)
        self.connected_listbox.bind('<ButtonRelease-1>', self.on_drop)

    def on_select(event):
        widget = event.widget
        selected_item = widget.selection()[0]
        widget._drag_data = {
            "item": selected_item,
            "values": widget.item(selected_item, "values"),
            "parent": widget.parent(selected_item)
        }

    def on_drop(self, event: tk.Event) -> None:
        widget = event.widget
        try:
            if widget._drag_data is not None:
                print(f"Drop event at coordinates: ({event.x_root}, {event.y_root})")
                target_widget = widget.winfo_containing(event.x_root, event.y_root)
                if target_widget is not None and widget._drag_data["parent"] != self.connected_listbox and target_widget == self.connected_listbox:
                    if widget._drag_data["item"] not in self.connections:
                        self.connections.append(widget._drag_data["item"])
                        self.update_listbox()
        except IndexError as e:
            logging.error(f"Error in on_drop method: {e}")

    def on_drag(self, event: tk.Event) -> None:
        widget = event.widget
        if not hasattr(widget, '_drag_data') or widget._drag_data is None:
            return

        # Update the drag data with the current mouse position
        widget._drag_data["x"] = event.x
        widget._drag_data["y"] = event.y

        # Optionally, you can add visual feedback for dragging here
        # For example, changing the cursor or highlighting the item