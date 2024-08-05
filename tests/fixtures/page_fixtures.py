
import pytest

from UI.pages.requirements.add_requirement import AddRequirementPage
from UI.pages.requirements.edit_requirement import EditRequirementPage
from tests.mocks.mock_main_app import MockMainApplication


def create_and_show_page(app: MockMainApplication, page_class, requirement=None):
    page = page_class(app)
    if requirement:
        page.requirement = requirement
    page.create_body()
    page.show()
    return page


@pytest.fixture
def edit_requirement_page(app, request):
    requirement = request.param
    page = create_and_show_page(app, EditRequirementPage, requirement)
    yield page

@pytest.fixture
def add_requirement_page(app):
    page = create_and_show_page(app, AddRequirementPage)
    yield page
