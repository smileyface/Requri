
import tkinter as tk


class AutoCompleteEntry(tk.Frame):
    def __init__(self, master, choices, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.choices = list(choices)
        self.popup = None
        self.in_state = False

        self.current_text = None

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.option_list = tk.Listbox(self, selectmode=tk.SINGLE)

        self.entry.bind('<KeyRelease>', self.check_trigger)
        self.entry.bind('<KeyPress>', self.backspaces)

        self.option_list.bind('<Double-Button-1>', self.add_choices_from_popup)

    @property
    def list(self):
        entries = self.entry.get().split(",")
        for x in range(len(entries)):
            entries[x] = entries[x].strip().strip("#")
        if '' in entries:
            entries.remove('')
        return entries

    @list.setter
    def list(self, value):
        if isinstance(value, list):
            self.entry.insert(0, "#" + ", #".join(value) + ",")
        else:
            raise ValueError

    def check_trigger(self, event):
        if event.keysym == 'numbersign' and self.in_state is False:
            self.show_popup()
            self.in_state = True
        elif event.keysym == 'comma' and self.option_list.winfo_ismapped() and self.in_state is True:
            self.add_current_text_to_popup()
            self.in_state = False
        else:
            if self.in_state is True:
                self.current_text += event.char
                self.update_options()

    def backspaces(self, event):
        if event.keysym == 'BackSpace':
            if self.current_text != "" and self.in_state is True:
                self.current_text = self.current_text[:-1]
            elif self.entry.get()[-1] == ",":
                self.in_state = True
                self.show_popup()
                self.current_text = self.entry.get().split("#")[-1][:-1]
            else:
                self.in_state = False
                self.option_list.pack_forget()

    def show_popup(self):
        self.current_text = ""
        if not self.option_list.winfo_ismapped():
            self.update_options()
            self.option_list.pack(fill=tk.BOTH, expand=True)

    def add_current_text_to_popup(self):
        self.choices.append(self.current_text)
        self.option_list.pack_forget()

    def add_choices_from_popup(self, event):
        index = self.option_list.curselection()
        if index:
            selected_text = self.option_list.get(index)
            autocompleted_entry = self.list
            autocompleted_entry[-1] = selected_text
            strong = "#" + ", #".join(autocompleted_entry) + ","
            self.entry.delete(0, tk.END)  # Clear existing text
            self.entry.insert(0, strong)  # Insert new text
            self.current_text = selected_text
            self.in_state = False
            self.option_list.pack_forget()

    def update_options(self):
        self.option_list.delete(0, tk.END)
        choices = self.get_options()
        for choice in choices:
            self.option_list.insert(tk.END, choice)

    def get_options(self):
        options = []
        if self.current_text:
            for choice in self.choices:
                if self.current_text in choice and len(options) < 5:
                    options.append(choice)
        else:
            options = self.choices[:5]
        return options

    def update_choices(self, choices):
        self.choices = choices