import tkinter as tk

from UI.pages.paging_handle import get_page, PagesEnum, show_page


class RequirementFrame(tk.Frame):
    def __init__(self, master, requirement, **kwargs):
        super().__init__(master, bd=1, relief=tk.SOLID, **kwargs)
        self.master = master
        self.requirement = requirement
        label_text = requirement.unique_id.to_string()
        self.uid = tk.Label(self, text=label_text, width=10)  # Set the width as needed
        self.uid.pack(side=tk.LEFT, padx=5, pady=5)  # Adjust padding as needed

        req_text = requirement.text
        self.label = tk.Label(self, text=req_text)
        self.label.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.label.bind("<Double-1>", self.on_double_click)

    def get_requirement(self):
        return self.requirement

    def on_double_click(self, event):
        get_page(PagesEnum.EDIT_REQUIREMENT).requirement = self.requirement
        show_page(PagesEnum.EDIT_REQUIREMENT)