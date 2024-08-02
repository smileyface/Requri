# test_main_application.py

from UI.main_app import MainApplication
import pytest
from UI.menubars.main import MainMenuBar
from UI.pages.paging_handle import PagingHandle, PagesEnum


@pytest.fixture
def app():
    app = MainApplication()
    yield app
    app.destroy()


class TestMainApplication:

    def test_initialization_title_and_dimensions(self, app):
        assert app.title() == "Requirement Tracker"
        width_height = app.geometry().split('+')[0]  # Extract the width and height part
        assert width_height == "900x765"

    def test_navigation_bar_creation(self, app):
        assert app.page_back_button.winfo_exists()
        assert app.page_forward_button.winfo_exists()
        assert app.context_action_box.winfo_exists()

    def test_menu_bar_creation(self, app):
        assert isinstance(app.children['!mainmenubar'], MainMenuBar)

    def test_pages_registration(self, app):
        assert PagesEnum.RECORD_VIEW in PagingHandle._page_map
        assert PagesEnum.ADD_REQUIREMENT in PagingHandle._page_map
        assert PagesEnum.EDIT_REQUIREMENT in PagingHandle._page_map
        assert PagesEnum.MASS_ADD_REQUIREMENT in PagingHandle._page_map
        assert PagesEnum.REQUIREMENT_EXTENDED in PagingHandle._page_map

    def test_initial_page_display(self, app):
        current_page_enum = PagingHandle.get_current_page()
        assert current_page_enum == PagesEnum.RECORD_VIEW

    def test_incorrect_page_enum_registration(self):
        with pytest.raises(KeyError):
            PagingHandle.create_and_register_page(None, "INVALID_PAGE", None)

    def test_missing_or_incorrect_page_enum_values(self, app):
        with pytest.raises(KeyError):
            PagingHandle.show_page(10)
        with pytest.raises(KeyError):
            PagingHandle.show_page("INVALID_PAGE_ENUM")

    def test_context_action_box_updates(self, app):
        initial_page = app.page_container.winfo_children()[0]
        initial_page.create_context_nav()
        initial_context_children = app.context_action_box.winfo_children()
        print(f"Initial Context Children: {initial_context_children}")  # Debug print

        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)
        app.update_idletasks()  # Ensure UI updates

        new_page = app.page_container.winfo_children()[0]
        new_page.create_context_nav()
        new_context_children = app.context_action_box.winfo_children()
        print(f"New Context Children: {new_context_children}")  # Debug print

        assert len(initial_context_children) != len(new_context_children)

    def test_page_container_display_single_page(self, app):
        pages = app.page_container.winfo_children()
        visible_pages = [page for page in pages if page.winfo_ismapped()]
        assert len(visible_pages) == 1


    def test_app_tree_is_displayed(self, app):
        assert app.winfo_ismapped() == 1
        assert app.page_container.winfo_ismapped() == 1
        assert app.page_container.children['!recordsview'].winfo_ismapped()
