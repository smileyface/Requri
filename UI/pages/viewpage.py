import tkinter as tk


class ViewPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master

    def show(self):
        if self.master.current_page:
            self.master.current_page.pack_forget()
        self.pack(in_=self.master.page_container)
        self.master.current_page = self

    def hide(self):
        self.pack_forget()
