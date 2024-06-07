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

    def make_trace_tab(self, master):
        tab = ttk.Frame(master)
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
