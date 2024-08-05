import tkinter as tk
import webbrowser


class HyperlinkEntry(tk.Text):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.tag_configure("hyperlink", foreground="blue", underline=True)
        self.bind("<Button-1>", self.on_click)
        self.link_words = []

    def insert_hyperlinks(self, text, urls):
        words = text.split()
        for word in words:
            if word in self.link_words:
                self.insert_word_hyperlink(word, urls[word])
            else:
                self.insert(tk.END, word + " ")

    def insert_word_hyperlink(self, word, url):
        self.insert(tk.END, word + " ", "hyperlink")
        self.tag_bind("hyperlink", "<Button-1>", lambda event: webbrowser.open_new(url))

    def on_click(self, event):
        index = self.index("@{},{}".format(event.x, event.y))
        tags = self.tag_names(index)
        if "hyperlink" in tags:
            return "break"  # Prevent default behavior when clicking on hyperlink

    def on_key_release(self, event):
        if event.keysym in ["space", "period", "comma", "exclam", "question"]:
            self.insert_hyperlinks_from_list()
        elif event.keysym == "BackSpace":
            self.backspace_hyperlink_check()

    def insert_hyperlinks_from_list(self):
        current_index = self.index(tk.INSERT)
        prev_char = self.get(current_index + "-1c")
        if prev_char.isspace() or prev_char in [".", ",", "!", "?"]:
            current_word = self.get("insert linestart", "insert").strip()
            if current_word in self.link_words:
                url = self.link_words[current_word]
                self.insert_word_hyperlink(current_word, url)

    def backspace_hyperlink_check(self):
        current_index = self.index(tk.INSERT)
        prev_char = self.get(current_index + "-1c")
        if prev_char.isspace() or prev_char in [".", ",", "!", "?"]:
            self.delete("insert-2c", "insert")  # Remove the hyperlink if backspacing at word boundary
