import tkinter as tk
from tkinter import ttk

from structures import requirement_list
from UI.pages.paging_handle import show_page, PagesEnum, get_page


class RequirementsDisplayMain(ttk.Treeview):

    def __init__(self, master, **kwargs):
        super().__init__(master, columns=("ID", "Text"), **kwargs)

        self.heading("#0", text="ID")
        self.heading("#1", text="Text")

        self.update()

        self.bind("<Delete>", self.remove_selected)
        self.bind("<Double-1>", self.edit_selected)

    def add(self, requirement):
        requirement_str = requirement.unique_id.to_string()
        self.insert("", tk.END, text=requirement_str, values=(requirement.text,))

    def remove(self, index):
        requirement_list.remove(requirement_list.get_requirement_from_index_string(index))

    def remove_selected(self, event):
        selection = self.selection()
        if selection:
            selected_item = self.item(selection[0])
            requirement_key = selected_item['text']  # Assuming the key is in the first column
            self.remove(requirement_key)
        self.update()

    def edit_selected(self, event):
        selection = self.selection()
        if selection:
            selected_item = self.item(selection[0])
            requirement_key = selected_item['text']
            requirement = requirement_list.get_requirement_from_index_string(requirement_key)
            if requirement:
                get_page(PagesEnum.EDIT_REQUIREMENT).requirement = requirement
                show_page(PagesEnum.EDIT_REQUIREMENT)


    def update(self):
        # Clear the Tree View
        for item in self.get_children():
            self.delete(item)

        requirement_map = requirement_list.get_requirement_map()
        sorted_keys = sorted(requirement_map.keys(), key=lambda x: (x[0], x[1]))
        # Iterate over the sorted keys and access the corresponding requirement maps
        for requirement_section in sorted_keys:
            for requirement in requirement_map[requirement_section].values():
                self.add(requirement)
