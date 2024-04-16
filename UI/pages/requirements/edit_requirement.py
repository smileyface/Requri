import tkinter as tk
from UI.pages.requirements.add_requirement import AddRequirementPage, get_variable
from structures import requirement_list
from structures.requirement import Requirement


class EditRequirementPage(AddRequirementPage):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.requirement = None
        self.add_button.configure(text="Edit", command=self.edit)

    def edit(self):
        requirement_list[(self.requirement.unique_id.section, self.requirement.unique_id.subsection)][
            self.requirement.unique_id.unique_id] = Requirement(get_variable(self.section),
                                                                get_variable(self.subsection),
                                                                self.title_entry.get(),
                                                                self.requirement_text.get("1.0", tk.END), [])
        return self.requirement

    def on_show(self):
        # Populate fields with data from the provided Requirement instance
        self.title_entry.insert(0, self.requirement.title)
        self.section.variable.set(self.requirement.unique_id.section)
        self.update_combobox_b()  # Update subsection combobox based on section
        self.subsection.variable.set(self.requirement.unique_id.sub)
        self.requirement_text.insert("1.0", self.requirement.text)