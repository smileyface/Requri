import logging
import tkinter as tk
from tkinter import ttk
from typing import List, Union, Any

from UI.pages.viewpage import ViewPage
from structures.records import *


def get_variable(var):
    return var.variable.get().replace('\'', '')


class AddRequirementPage(ViewPage):
    def __init__(self, parent_widget, *args: Any, **kwargs: Any):
        super().__init__(parent_widget, args, kwargs)
        self.connections = None

    def on_drop(self, event: tk.Event) -> None:
        try:
            widget = event.widget
            if widget._drag_data is None:
                return
            if widget._drag_data:
                target_widget = widget.winfo_containing(event.x_root, event.y_root)
                if widget._drag_data["parent"] != self.connected_listbox and target_widget == self.connected_listbox:
                    if widget._drag_data["item"] not in self.connections:
                        self.connections.append(widget._drag_data["item"])
                        self.update_listbox()
        except Exception as e:
            logging.error(f"Error in on_drop method: {e}")

    def on_select(self, event):
        selected_item = event.widget.selection()
        if selected_item:
            item = event.widget.item(selected_item)
            logging.info(f"Selected item: {item['text']}")

    def on_drag(self, event: tk.Event) -> None:
        try:
            widget = event.widget
            if widget._drag_data is None:
                widget._drag_data = {"x": event.x, "y": event.y, "item": widget.selection(), "parent": widget}
            else:
                dx = event.x - widget._drag_data["x"]
                dy = event.y - widget._drag_data["y"]
                widget.move(widget._drag_data["item"], dx, dy)
        except Exception as e:
            logging.error(f"Error in on_drag method: {e}")

    def get_list_of_type(self, input_list: List[Any], _type: type) -> List[Any]:
        """
        Filter a list based on a specific type.

        Args:
            input_list (list): The input list to filter.
            _type (type): The type to filter the list with.

        Returns:
            list: A filtered list containing only elements of the specified type.
        """
        if not isinstance(_type, type):
            raise TypeError("`_type` must be a valid type")
        return [x for x in input_list if isinstance(x, _type)]

    def _add_lists_to_treeview(self, connected: List[Union[Code, Requirement]], treeview: ttk.Treeview) -> None:
        code_list = self.get_list_of_type(connected, Code)
        requirements_list = self.get_list_of_type(connected, Requirement)

        for item_list, item_type, item_text, item_prefix in [(requirements_list, "Requirement", "Related Requirements", "Req-"),
                                                             (code_list, "Code", "Implementations", "Code-")]:
            for item in item_list:
                item_id = treeview.insert("", "end", text=item_text)
                try:
                    if item.unique_id is None:
                        logging.error(f"{item_type} item has no unique_id: {item}")
                        continue  # Skip items with None unique_id
                    treeview.insert(item_id, "end", text=item, iid=f"{item_prefix}{str(item.unique_id)}")
                except Exception as e:
                    logging.error(f"Error inserting {item_type} item: {e}")
                    raise e

    def create_body(self):
        print("AddRequirementView body created")

        notebook = ttk.Notebook(self.master)
        notebook.pack(fill='both', expand=True)

        requirement_tab = self.make_requirement_tab()
        trace_tab = self.make_trace_tab()

        notebook.add(requirement_tab, text='Add Requirement')
        notebook.add(trace_tab, text='Traceability')

    def make_trace_tab(self):
        tab = ttk.Frame(self.master)
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

        return tab

    def make_requirement_tab(self):
        tab = ttk.Frame(self.master)

        # Create labels and entry fields for each attribute of Requirement
        labels = ["Section", "Subsection", "Title", "Text", "Tags"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(tab)
            if label == "Text":
                entry = ttk.Entry(tab, width=50)  # Adjust width as needed
                entry.grid(row=i, column=1, columnspan=2, padx=10, pady=5, sticky=tk.EW)
                tab.grid_rowconfigure(i, weight=1)  # Allow row to expand
                tab.grid_columnconfigure(1, weight=1)  # Allow column to expand
            else:
                entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.EW)
            self.entries[label.lower()] = entry

        # Add a submit button
        submit_button = ttk.Button(tab, text="Submit", command=self.submit_requirement)
        submit_button.grid(row=len(labels), column=0, columnspan=3, pady=10)

        return tab

    def submit_requirement(self):
        # Retrieve the data from the entry fields
        section = self.entries["section"].get()
        sub = self.entries["subsection"].get()
        title = self.entries["title"].get()
        text = self.entries["text"].get()
        tags = self.entries["tags"].get().split(',')

        # Create a new Requirement object
        new_requirement = Requirement(section, sub, title, text, tags)

        # Add the new requirement to the connections list
        if self.connections is None:
            self.connections = []
        self.connections.append(new_requirement)

        # Update the connected listbox
        self.update_listbox()

        # Clear the entry fields
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def update_listbox(self):
        # Clear the current items in the connected listbox
        for item in self.connected_listbox.get_children():
            self.connected_listbox.delete(item)

        # Add the updated connections to the connected listbox
        self._add_lists_to_treeview(self.connections, self.connected_listbox)