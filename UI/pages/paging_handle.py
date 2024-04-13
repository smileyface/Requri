from enum import Enum
import tkinter as tk

_current_page = None
_frame_map = dict()
_page_map = dict()
_pages = []


class PagesEnum(Enum):
    MAIN = 1
    ADD_REQUIREMENTS = 2


def show_page(page_enum):
    global _current_page
    frame = _frame_map.get(page_enum)
    if frame:
        if _current_page:
            _current_page.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)
        _page_map[page_enum].update()
        _current_page = frame
    else:
        raise ValueError("Page not found")


def get_page(page_enum):
    return _page_map[page_enum]


def create_and_register_frame(parent, page_enum, page_type):
    frame = tk.Frame(parent)
    page = page_type(frame)
    page.pack(fill=tk.BOTH, expand=True)
    _frame_map[page_enum] = frame
    _page_map[page_enum] = page
