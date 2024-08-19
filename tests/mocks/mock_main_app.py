from src.UI.main_app import MainApplication


class MockMainApplication(MainApplication):
    def __init__(self):
        super().__init__()
        self.title("Mock Main Application")
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)
        widget.pack()

    def remove_widget(self, widget):
        self.widgets.remove(widget)
        widget.pack_forget()

    def destroy(self):
        for widget in self.widgets:
            widget.destroy()
        super().destroy()

    def run(self):
        self.mainloop()  # Start the main loop