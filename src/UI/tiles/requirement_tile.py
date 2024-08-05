import tkinter as tk

from UI.tiles.tile import Tile


class RequirementTile(Tile):

    default_width = 30  # Example default width

    def create_widgets(self):
        # Title
        self.title = tk.Label(self, text=self.data.title, width=self.default_width, font=("Helvetica", 12, "bold"))
        self.title.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Text
        self.label = tk.Label(self, text=self.data.text, wraplength=300, height=7, justify="left")
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Tags
        tags_text = "Tags: #" + ", #".join(self.data.tags)
        self.tags_label = tk.Label(self, text=tags_text, wraplength=300)
        self.tags_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    def update_widgets(self):
        self.title.config(text=self.data.title)
        self.label.config(text=self.data.text)
        tags_text = "Tags: #" + ", #".join(self.data.tags)
        self.tags_label.config(text=tags_text)