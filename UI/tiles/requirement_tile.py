import tkinter as tk

from UI.tiles.tile import Tile


class RequirementTile(Tile):

    def __init__(self, master, requirement, **kwargs):
        super().__init__(master, requirement, **kwargs)

        # Title
        label_text = requirement.title
        self.title = tk.Label(self, text=label_text, width=self.default_width, font=("Helvetica", 12, "bold"))
        self.title.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Text
        req_text = requirement.text
        self.label = tk.Label(self, text=req_text, wraplength=300, height=7, justify="left")
        self.label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Tags (if available)
        tags_text = "Tags: #" + ", #".join(requirement.tags)
        self.tags_label = tk.Label(self, text=tags_text, wraplength=300)
        self.tags_label.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Bind events for the label
        self.bind_child_events()
