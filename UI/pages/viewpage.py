import tkinter as tk
from tkinter import ttk
from typing import Any

from UI.pages import paging_handle


class ViewPage(tk.Frame):
    def __init__(self, parent_widget, *args: Any, **kwargs: Any) -> None:
            """
            Initializes an instance of the ViewPage class.

            Args:
                parent_widget: The parent widget.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Attributes:
                parent_widget: The parent widget.
                main_app_body: The main application body frame.
                context_action_box: The context action box widget.
            """
            super().__init__(parent_widget)
            self.parent_widget = parent_widget
            self.main_app_body = ttk.Frame(self.parent_widget)
            self.context_action_box = None

            if hasattr(self.parent_widget, 'master') and hasattr(self.parent_widget.master, 'master') and hasattr(self.parent_widget.master.master, 'master') and hasattr(self.parent_widget.master.master.master, 'context_action_box'):
                self.context_action_box = self.parent_widget.master.master.master.context_action_box
            else:
                pass
                # Handle the case where the attribute does not exist

    def create_body(self):
        raise NotImplementedError("Subclasses should implement this!")

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
