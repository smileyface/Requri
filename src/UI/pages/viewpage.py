import logging
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk
from typing import Any


class ViewPage(ABC, tk.Frame):
    def __init__(self, master, *args: Any, **kwargs: Any) -> None:
        """
        Initializes an instance of the ViewPage class.

        Args:
            master: The parent widget.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Attributes:
            master: The parent widget.
            main_app_body: The main application body frame.
            context_action_box: The context action box widget.
        """
        if master is None:
            raise AttributeError("No parent container passed in")
        super().__init__(master)
        self.master = master
        self.context_action_box = self._get_context_action_box()
        self.displayed = False

    def _get_context_action_box(self):
        parent = self.master
        while parent:
            if hasattr(parent, 'context_action_box'):
                return parent.context_action_box
            parent = parent.master
        # Fallback if not found
        return ttk.Frame(self.master, name="unattached_context_action_frame")

    @abstractmethod
    def create_body(self) -> None:
        """
        This is where the components of a page are created.

        Placeholder method to be overridden by subclasses.
        """
        logging.info(f"{type(self).__name__} body created")

    @abstractmethod
    def create_context_nav(self) -> None:
        """
        Placeholder method intended to be overridden by subclasses.
        """
        pass

    @abstractmethod
    def display_body(self):
        """
        This is where the components of a page are packed.

        Placeholder method intended to be overridden by subclasses.

        """
        pass

    def to_string(self):
        return f"{type(self)}"

    def on_show(self):
        """
        This is for page specific commands when page is about to be displayed.
        This is to be inherited when needed.
        """
        pass

    def on_hide(self):
        for widget in self.context_action_box.winfo_children():
            widget.destroy()

    def show(self):
        if self.displayed:
            return
        self.display_body()
        self.create_context_nav()
        self.on_show()
        self.displayed = True

    def hide(self):
        if not self.displayed:
            return
        self.pack_forget()
        self.on_hide()
        self.displayed = False

    def update(self):
        pass
