import tkinter as tk

from UI.pages.paging_handle import get_page, PagesEnum, show_page


class RequirementTile(tk.Frame):
    width = 25
    def __init__(self, master, requirement, **kwargs):
        super().__init__(master, bd=1, relief=tk.SOLID, **kwargs)
        self.selected = False
        self.master = master
        self.requirement = requirement

        # Title
        label_text = requirement.title
        self.title = tk.Label(self, text=label_text, width=RequirementTile.width, font=("Helvetica", 12, "bold"))
        self.title.grid(row=0, column=0, columnspan=2, pady=5, sticky="n")

        # Text
        req_text = requirement.text
        self.label = tk.Label(self, text=req_text, wraplength=300, height=7, justify="left")
        self.label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Tags (if available)
        tags_text = "Tags: " + ", ".join(requirement.tags)
        self.tags_label = tk.Label(self, text=tags_text, wraplength=300)
        self.tags_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.label.bind("<Double-1>", self.on_double_click)  # Edit requirement when double clicking the title
        self.bind("<Button-1>", self.toggle_selection)  # Bind click event to toggle selection
        self.title.bind("<Button-1>", self.toggle_selection)

    def get_requirement(self):
        return self.requirement

    def on_double_click(self, event):
        get_page(PagesEnum.EDIT_REQUIREMENT).requirement = self.requirement
        show_page(PagesEnum.EDIT_REQUIREMENT)

    def toggle_selection(self, event):
        if not self.selected:
            self.select()
        else:
            self.deselect()

    def select(self):
        self.selected = True
        self.config(borderwidth=2, relief=tk.SOLID, highlightbackground="blue")

    def deselect(self):
        self.selected = False
        self.config(borderwidth=1, relief=tk.SOLID)
