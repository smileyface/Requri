import tkinter as tk

from UI.pages.paging_handle import page_return
from UI.pages.requirements.add_requirement import AddRequirementPage, get_variable
from structures import requirement_list
from structures.requirement import Requirement


class MassAddRequirementPage(AddRequirementPage):
    def __init__(self, master):
        super().__init__(master)


    def add(self):
        texts = self.requirement_text.get("1.0", tk.END).strip().split("\n")
        for text in texts:
            req = Requirement(get_variable(self.section), get_variable(self.subsection), self.title_entry.get(),
                              text, self.tagging_text.list)
            requirement_list.append(req)
        page_return()
