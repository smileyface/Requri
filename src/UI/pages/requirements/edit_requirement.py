import tkinter as tk

import src.UI.pages.paging_handle as PagingHandle
from src.UI.pages.requirements.add_requirement import AddRequirementPage, get_variable
from src.structures.lists import requirement_list


class EditRequirementPage(AddRequirementPage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.requirement = None

    def edit(self):
        requirement_list.update(self.requirement.unique_id, get_variable(self.section), get_variable(self.subsection),
                                self.title_entry.get(), self.requirement_text.get("1.0", tk.END),
                                self.tagging_text.list)
        PagingHandle.page_return()

    def create_context_nav(self):
        super().create_context_nav()
        self.add_button.configure(text="Edit", command=self.edit)

    def on_hide(self):
        super().on_hide()
        self.requirement_text.delete("1.0", tk.END)  # Clear existing text
        self.title_entry.delete(0, tk.END)  # Clear existing text
        self.tagging_text.clear()

    def on_show(self):
        super().on_show()
        if self.requirement is None:
            raise ValueError("Requirement is not set. Cannot show the page.")
        # Populate fields with data from the provided Requirement instance
        self.title_entry.insert(0, self.requirement.title)  # Insert new text
        self.section.variable.set(self.requirement.unique_id.section)
        self.update_combobox_b()  # Update subsection combobox based on section
        self.subsection.variable.set(self.requirement.unique_id.sub)
        self.requirement_text.insert("1.0", self.requirement.text)  # Insert new text
        self.tagging_text.list = self.requirement.tags
