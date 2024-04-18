import tkinter as tk
from UI.components.autocomplete_popup import AutoCompletePopup


class AutoCompleteEntry(tk.Entry):
    def __init__(self, master, choices, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.choices = choices
        self.popup = None

        self.bind('<KeyPress>', self.check_trigger)

    def check_trigger(self, event):
        if event.char == '#' and not self.popup:
            self.popup = AutoCompletePopup(self.master, self.choices)
            x, y, _, h = self.bbox(tk.END)
            x += self.winfo_rootx() + 25
            y += self.winfo_rooty() + h
            self.popup.geometry("+{}+{}".format(x, y))
            self.popup.lift()
            self.focus_set()
        elif event.char == ',' and self.popup:
            text = self.popup.text_var.get()
            if text:
                self.choices.append(text)
                # Split the text by commas and trigger autocomplete for each tag
                tags = [tag.strip() for tag in text.split(',')]
                for tag in tags:
                    self.trigger_autocomplete(tag)

    def trigger_autocomplete(self, tag):
        # Implement auto-complete behavior for the tag
        print("Auto-complete triggered for tag:", tag)
