import os
import tkinter as tk

from src.UI.tiles.tile import Tile


class CodeTile(Tile):

    def get_url_text(self):
        url_text = ""
        if self.data.declaration:
            url_text += f"Decl: {self.data.declaration.path}"
        if self.data.declaration and self.data.definition:
            url_text += "\n"
        if self.data.definition:
            url_text += f"Def: {self.data.definition.path}"
        return url_text

    def create_widgets(self):
        # Create labels for URL and name
        name_text = f"{self.data.class_name}::{self.data.name}({', '.join(self.data.arguments)})" if not os.path.exists(
            self.data.class_name) else f"{self.data.name}({', '.join(self.data.arguments)})"
        url_text = self.get_url_text()

        self.name_label = tk.Label(self, text=name_text, width=25, font=("Helvetica", 10, "bold"))
        self.name_label.pack(side=tk.TOP, fill=tk.X, pady=5)
        self.url_label = tk.Label(self, wraplength=300, text=url_text)
        self.url_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def update_widgets(self):
        name_text = f"{self.data.class_name}::{self.data.name}({', '.join(self.data.arguments)})" if not os.path.exists(
            self.data.class_name) else f"{self.data.name}({', '.join(self.data.arguments)})"
        url_text = self.get_url_text()

        self.name_label.config(text=name_text)
        self.url_label.config(text=url_text)
