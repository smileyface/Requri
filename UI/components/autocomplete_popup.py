import tkinter as tk

class AutoCompletePopup(tk.Toplevel):
    def __init__(self, master, choices):
        super().__init__(master)
        self.master = master
        self.choices = choices
        self.matches = []

        self.text_var = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.text_var)
        self.entry.pack()

        self.listbox = tk.Listbox(self, height=5)
        self.listbox.pack()

        self.entry.bind('<KeyRelease>', self.update_matches)
        self.entry.bind('<Return>', self.select_match)

    def update_matches(self, event):
        self.matches.clear()
        text = self.text_var.get()
        if '#' in text:
            prefix, _ = text.split('#', maxsplit=1)
            prefix = prefix.strip()
            if prefix:
                self.matches = [choice for choice in self.choices if choice.startswith(prefix)]
                self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for match in self.matches[:5]:
            self.listbox.insert(tk.END, match)

    def select_match(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_text = self.listbox.get(selected_index[0])
            self.text_var.set(selected_text)
            self.matches.clear()
            self.listbox.delete(0, tk.END)
            self.entry.icursor(tk.END)
                                                                                                                                                                                                                                                        