import tkinter as tk

import src.UI.pages.paging_handle as PagingHandle
from src.UI.pages.requirements.add_requirement import AddRequirementPage, get_variable
from src.structures.lists import requirement_list
from src.structures.records.requirement import Requirement


class MassAddRequirementPage(AddRequirementPage):
    def __init__(self, master):
        super().__init__(master)

    def add(self):
        texts = self.requirement_text.get("1.0", tk.END).strip().split("\n")
        for text in texts:
            req = Requirement(get_variable(self.section), get_variable(self.subsection), self.title_entry.get(),
                              text, self.tagging_text.list)

            requirement_list.append(req)
        PagingHandle.page_return()
  