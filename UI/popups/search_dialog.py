import tkinter as tk
from tkinter import simpledialog


class SearchDialog(simpledialog.Dialog):
    def __init__(self, master, search_options):
        def body(self, master):
            tk.Label(master, text="Search Query:").grid(row=0, column=0)
            self.search_entry = tk.Entry(master)
            self.search_entry.grid(row=0, column=1)

            self.search_option = tk.StringVar(master)
            self.search_option.set("Text")  # Default to searching by text
            tk.OptionMenu(master, self.search_option, "Text", "Tag").grid(row=1, column=1, sticky="ew")

            return self.search_entry

        def apply(self):
            query = self.search_entry.get()
            search_option = self.search_option.get()
            self.result = (search_option, query)  # You can do something with the search query and option here

            # Perform search based on the selected option
            if search_option == "Text":
                self.text_search(query)
            elif search_option == "Tag":
                self.tag_search(query)

        def text_search(self, query):
            # Implement text search logic here
            pass

        def tag_search(self, query):
            # Implement tag search logic here
            pass
