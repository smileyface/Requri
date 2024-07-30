from functools import wraps
import pytest
from UI.pages.paging_handle import PagingHandle, PagesEnum

def main_app_test(page_enum):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            result = False
            exception = []
            try:
                PagingHandle.show_page(page_enum, forgo_stack=True)
                kwargs['page'] = PagingHandle.get_page(page_enum)
                result = test_func(*args, **kwargs)
            except Exception as e:
                exception.append(e)
            if exception:
                raise exception[0]
            return result
        return wrapper
    return decorator

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
