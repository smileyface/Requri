import logging
import tkinter as tk

from src.UI.components.tile_display import TileView
from src.UI.pages.viewpage import ViewPage


class RecordsView(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.label = None
        self.requirement_listbox = None

    def create_body(self):
        logging.info(f"{type(self).__name__} body created")
        self.label = tk.Label(self, text="Requirements:")
        self.requirement_listbox = TileView(self)

    def display_body(self):
        self.label.pack(fill=tk.X)
        self.requirement_listbox.pack(fill=tk.BOTH, expand=True)

    def create_context_nav(self) -> None:
        pass

    def on_show(self):
        self.update()
        super().on_show()

    def update(self):
        self.requirement_listbox.update()
