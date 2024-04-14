import tkinter as tk
from tkinter import Entry, Toplevel, Listbox


class AutocompleteEntry(tk.Entry):
    def __init__(self, master=None, autocomplete_list=[], **kwargs):
        self.autocomplete_list = autocomplete_list
        self.recent_tags = []
        self.var = tk.StringVar()
        tk.Entry.__init__(self, master, textvariable=self.var, **kwargs)
        self.var.trace('w', self.changed)
        self.listbox = None

    def on_key_press(self, event):
        if event.char == '#':
            self.show()

    def on_enter(self, event):
        self.hide()

    def on_escape(self, event):
        self.hide()

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.hide()
        elif self.var.get() == '#':
            words = self.recent_tags
        else:
            words = self.comparison()
            if words:
                self.update(words)
                self.show()
            else:
                self.hide()

    def comparison(self):
        returner = []
        for word in self.autocomplete_list:
            if self.var.get().lower().replace("#", "") in word.lower():
                returner.append("#" + word)
        return returner

    def update(self, words):
        if not self.listbox:
            self.listbox = tk.Listbox(self.master, width=self.winfo_width())
            self.listbox.bind("<Button-1>", self.on_select)
            self.listbox.bind("<Return>", self.on_select)
            self.listbox.bind("<Escape>", self.hide)
        self.listbox.delete(0, tk.END)
        for word in words:
            self.listbox.insert(tk.END, word)
        x, y = self.winfo_rootx(), self.winfo_rooty() + self.winfo_height()
        self.listbox.place(x=x, y=y + 1)

    def show(self):
        if self.listbox:
            self.listbox.lift()

    def hide(self):
        if self.listbox:
            self.listbox.place_forget()

    def on_select(self, event):
        if self.listbox.curselection():
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.hide()
            self.focus_set()

    def set_autocomplete_list(self, autocomplete_list):
        self.autocomplete_list = autocomplete_list

    def set_listbox(self, listbox):
        self.listbox = listbox

    def show_recent_tags(self, event):
        if self.recent_tags:
            recent_tags_window = tk.Toplevel(self.master)
            recent_tags_window.title("Recent Tags")
            recent_tags_listbox = Listbox(recent_tags_window)
            for tag in self.recent_tags:
                recent_tags_listbox.insert(tk.END, tag)
            recent_tags_listbox.pack()

    def update_tags(self):
        tags = list(filter(None, self.get().split('#')))
        for x in tags:
            if x not in self.autocomplete_list:
                self.autocomplete_list.append(x)
            if x in self.recent_tags:
                self.recent_tags.remove(x)
            self.recent_tags.insert(0, x)
            self.recent_tags = self.recent_tags[:5]

        return tags
