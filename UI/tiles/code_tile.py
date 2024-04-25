import os
import tkinter as tk

from UI.tiles.tile import Tile


class CodeTile(Tile):
    def __init__(self, master, code, **kwargs):
        super().__init__(master, code, **kwargs)

        # Create labels for URL and name
        if os.path.exists(code.class_name):
            name_text = f"{code.name}({', '.join(code.argument)})"
        else:
            name_text = f"{code.class_name}::{code.name}({', '.join(code.argument)})"
        url_text = f"URL: {code.location}"
        name_label = tk.Label(self, text=name_text, width=25, font=("Helvetica", 10, "bold"))
        name_label.pack(side=tk.TOP, fill=tk.X, pady=5)
        url_label = tk.Label(self, wraplength=300, text=url_text)
        url_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self._selection_bind()

