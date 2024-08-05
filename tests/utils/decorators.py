from functools import wraps

import pytest

from UI.pages.paging_handle import PagingHandle


def main_app_test(page_enum):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(*args, **kwargs):
            result = False
            exception = []
            try:
                # Show the page and ensure it is initialized
                PagingHandle.show_page(page_enum, forgo_stack=True)
                kwargs['app'].update_idletasks()  # Ensure the UI is updated
                page = PagingHandle.get_page(page_enum)
                kwargs['page'] = page

                # Ensure the page is visible
                page.pack(expand=True, fill='both')
                page.update_idletasks()  # Ensure the page is updated


                # Run the main loop in a separate thread to handle events
                import threading

                def run_app():
                    kwargs['app'].run()

                app_thread = threading.Thread(target=run_app)
                app_thread.start()


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
