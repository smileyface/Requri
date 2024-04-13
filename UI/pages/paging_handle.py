from enum import Enum
import tkinter as tk

_current_page = None
_frame_map = dict()
_pages = []


class PagesEnum(Enum):
    MAIN = 1
    ADD_REQUIREMENTS = 2


def show_page(page_enum):
    global _current_page
    page = _frame_map.get(page_enum)
    if page:
        if _current_page:
            _current_page.pack_forget()
        page.pack(fill=tk.BOTH, expand=True)
        _current_page = page
    else:
        raise ValueError("Page not found")


def create_and_register_frame(parent, page_enum, page_type):
    frame = tk.Frame(parent)
    page = page_type(frame)
    page.pack(fill=tk.BOTH, expand=True)
    _frame_map[page_enum] = frame
    return page
