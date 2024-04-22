import tkinter as tk

from UI.components.tile import Tile


class RequirementTile(Tile):
    width = 25
    def __init__(self, master, requirement, **kwargs):
        super().__init__(master, requirement, **kwargs)

        # Title
        label_text = requirement.title
        self.title = tk.Label(self, text=label_text, width=RequirementTile.width, font=("Helvetica", 12, "bold"))
        self.title.grid(row=0, column=0, columnspan=2, pady=5, sticky="n")
        print(self.title.winfo_reqwidth())

        # Text
        req_text = requirement.text
        self.label = tk.Label(self, text=req_text, wraplength=300, height=7, justify="left")
        self.label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Tags (if available)
        tags_text = "Tags: " + ", ".join(requirement.tags)
        self.tags_label = tk.Label(self, text=tags_text, wraplength=300)
        self.tags_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.label.bind("<Double-1>", self.on_double_click)  # Edit requirement when double clicking the title
        self._selection_bind()



