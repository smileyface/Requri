import pytest

from UI.pages.viewpage import ViewPage
from testing.fixtures.app_fixtures import app
from testing.fixtures.view_page_fixture import test_page
from testing.mocks.mock_main_app import MockMainApplication


class TestViewPage:
    @pytest.mark.usefixtures("app", "test_page")
    def test_show_page(self, app: MockMainApplication, test_page: ViewPage):
        test_page.show()
        app.update()
        assert test_page.winfo_ismapped() == True

    @pytest.mark.usefixtures("app", "test_page")
    def test_hide_page(self, app: MockMainApplication, test_page: ViewPage):
        test_page.show()
        app.update_idletasks()  # Ensure all pending events are processed
        assert test_page.winfo_ismapped() == True
        test_page.hide()
        app.update_idletasks()  # Ensure all pending events are processed
        assert test_page.winfo_ismapped() == False

    @pytest.mark.usefixtures("app", "test_page")
    def test_display_body(self, app: MockMainApplication, test_page: ViewPage):
        test_page.display_body()
        app.update_idletasks()  # Ensure all pending events are processed
        assert test_page.winfo_ismapped() == True

    @pytest.mark.usefixtures("app", "test_page")
    def test_create_context_nav(self, app: MockMainApplication, test_page: ViewPage):
        test_page.create_context_nav()
        app.update_idletasks()  # Ensure all pending events are processed
        assert hasattr(test_page, 'add_button')
        assert hasattr(test_page, 'cancel_button')
