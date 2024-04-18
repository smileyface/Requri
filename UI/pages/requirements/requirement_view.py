from UI.pages.viewpage import ViewPage
import tkinter as tk

from UI.components.requirements_main_display import RequirementsDisplayMain


class RequirementView(ViewPage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.requirement_listbox = RequirementsDisplayMain(self.master)
        self.label = tk.Label(self.master, text="Requirements:")

        self.label.pack(fill=tk.X)
        self.requirement_listbox.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        self.requirement_listbox.update()
