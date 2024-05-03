import os
import tkinter as tk

from UI.tiles.tile import Tile
from structures import project


class CodeTile(Tile):
    def __init__(self, master, code, **kwargs):
        super().__init__(master, code, **kwargs)

        # Create labels for URL and name
        if os.path.exists(code.class_name):
            name_text = f"{code.name}({', '.join(code.arguments)})"
        else:
            name_text = f"{code.class_name}::{code.name}({', '.join(code.arguments)})"
        url_text = ""
        if code.declaration:
            url_text = f"Decl: {code.declaration.path}"
        if code.declaration and code.definition:
            url_text = url_text + "\n"
        if code.definition:
            url_text = url_text + f"Def:{code.definition.path}"
        name_label = tk.Label(self, text=name_text, width=25, font=("Helvetica", 10, "bold"))
        name_label.pack(side=tk.TOP, fill=tk.X, pady=5)
        url_label = tk.Label(self, wraplength=300, text=url_text)
        url_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Bind events for the label
        self.bind_child_events()

