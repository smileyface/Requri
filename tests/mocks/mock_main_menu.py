from UI.menubars.main import MainMenuBar

class MockMenuBar(MainMenuBar):
    def __init__(self):
        super().__init__(self.master)
        self.called = []

    def new_file(self):
        self.called.append("new_file")
