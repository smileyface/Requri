import pytest
import tkinter as tk


@pytest.fixture(scope="function")
def root():
    root = tk.Tk()
    yield root
    root.quit()
    root.destroy()
