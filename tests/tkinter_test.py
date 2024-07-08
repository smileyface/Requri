# tkinter_test.py

import tkinter as tk
from functools import wraps

import pytest


@pytest.fixture(scope="function")
def root():
    root = tk.Tk()
    yield root
    root.quit()
    root.destroy()


def tkinter_test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = []
        exception = []

        def run_func():
            try:
                result.append(func(*args, **kwargs))
            except Exception as e:
                exception.append(e)
            finally:
                kwargs['root'].quit()

        kwargs['root'].after(0, run_func)
        kwargs['root'].mainloop()

        if exception:
            raise exception[0]
        return result[0]

    return pytest.mark.usefixtures("root")(wrapper)
