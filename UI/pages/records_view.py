import tkinter as tk

from UI.components.tile_display import TileView
from UI.pages.viewpage import ViewPage


class RecordsView(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.label = None
        self.requirement_listbox = None
        self.master = master

    def create_body(self):
        self.label = tk.Label(self.master, text="Requirements:")
        self.requirement_listbox = TileView(self.master)

        self.label.pack(fill=tk.X)
        self.requirement_listbox.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        self.update()

    def update(self):
        self.requirement_listbox.update()
