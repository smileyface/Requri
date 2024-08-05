import tkinter as tk
from tkinter import ttk

import pytest

from UI.components.autocomplete_entry import AutoCompleteEntry
from UI.pages.paging_handle import PagesEnum
from UI.pages.requirements.edit_requirement import EditRequirementPage
from structures.lists import requirement_list
from structures.records import Requirement
from tests.fixtures.app_fixtures import app, page
from tests.fixtures.page_fixtures import edit_requirement_page
from tests.mocks.mock_main_app import MockMainApplication
from tests.utils.decorators import main_app_test

# Example requirements for tests
req_complete = Requirement("Section", "Subsection", "Title", "Text", ["Tag1"])
# noinspection PyTypeChecker
req_missing_fields = Requirement(None, None, None, None, [])


class TestEditRequirementPage:

    #  Initializes correctly with all required attributes
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_initializes_correctly_with_all_required_attributes(self, app: MockMainApplication,
                                                                edit_requirement_page: EditRequirementPage):
        assert edit_requirement_page.section is None
        assert edit_requirement_page.subsection is None
        assert edit_requirement_page.requirement_text is None
        assert edit_requirement_page.title_entry is None
        assert edit_requirement_page.tagging_text is None
        assert edit_requirement_page.master == app
        assert edit_requirement_page.requirement is None

    #  Updates requirement in requirement_list when edit method is called
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_updates_requirement_in_requirement_list_when_edit_method_is_called(self, app: MockMainApplication,
                                                                                edit_requirement_page: EditRequirementPage):
        requirement = Requirement("Section", "Subsection", "Title", "Text", [])
        requirement_list.append(requirement)
        edit_requirement_page.requirement = requirement
        edit_requirement_page.section.variable.set("New Section")
        edit_requirement_page.subsection.variable.set("New Subsection")
        edit_requirement_page.title_entry.insert(0, "New Title")
        edit_requirement_page.requirement_text.insert("1.0", "New Text")
        edit_requirement_page.tagging_text.insert(0, "New Tag")
        edit_requirement_page.edit()
        updated_requirement = requirement_list.get(requirement.unique_id)
        assert updated_requirement.section == "New Section"
        assert updated_requirement.subsection == "New Subsection"
        assert updated_requirement.title == "New Title"
        assert updated_requirement.text == "New Text"
        assert updated_requirement.tags == ["New Tag"]

    #  Changes button text to "Edit" and sets the command to edit in create_context_nav
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_changes_button_text_to_edit_and_sets_command_to_edit_in_create_context_nav(self, app: MockMainApplication,
                                                                                        edit_requirement_page: EditRequirementPage):
        edit_requirement_page.add_button = tk.Button(app)
        edit_requirement_page.create_context_nav()

        # Debugging print statements
        print(f"Button text: {edit_requirement_page.add_button.cget('text')}")
        print(f"Button command: {edit_requirement_page.add_button.cget('command')}")
        print(f"Expected command: {edit_requirement_page.edit}")

        assert edit_requirement_page.add_button.cget("text") == "Edit"
        assert edit_requirement_page.add_button.cget("command") == edit_requirement_page.edit

    #  Clears text fields and tagging list in on_hide
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_clears_text_fields_and_tagging_list_in_on_hide(self, app: MockMainApplication,
                                                            edit_requirement_page: EditRequirementPage):
        edit_requirement_page.requirement_text = tk.Text(app)
        edit_requirement_page.requirement_text.insert("1.0", "Some text")
        edit_requirement_page.title_entry = tk.Entry(app)
        edit_requirement_page.title_entry.insert(0, "Some title")
        edit_requirement_page.tagging_text = AutoCompleteEntry(app)
        edit_requirement_page.tagging_text.insert(0, "Some tag")
        edit_requirement_page.on_hide()
        assert edit_requirement_page.requirement_text.get("1.0", tk.END).strip() == ""
        assert edit_requirement_page.title_entry.get() == ""
        assert not len(edit_requirement_page.tagging_text.list)

    #  Populates fields with requirement data in on_show
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_populates_fields_with_requirement_data_in_on_show(self, app: MockMainApplication,
                                                               page: EditRequirementPage):
        requirement = Requirement("Section", "Subsection", "Title", "Text", ["Tag1"])
        requirement_list.append(requirement)
        page.requirement = requirement
        page.create_body()

        # Initialize fields that will be populated by on_show
        page.title_entry = tk.Entry(app)
        page.section = tk.StringVar()
        page.subsection = tk.StringVar()
        page.requirement_text = tk.Text(app)

        # Call on_show and check if it handles missing attributes gracefully
        try:
            page.on_show()
            assert True  # If no exception is raised, the test passes
            assert page.title_entry.get() == requirement.title
            assert page.section.get() == requirement.section
            assert page.subsection.get() == requirement.subsection
            assert page.requirement_text.get("1.0", tk.END).strip() == requirement.text
            assert list(page.tagging_text.get(0, tk.END)) == requirement.tags
        except Exception as e:
            pytest.fail(f"on_show raised an exception with missing attributes: {e}")

    #  Handles drag and drop events correctly in the traceability tab
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_drag_and_drop_events_correctly_in_traceability_tab(self, app: MockMainApplication,
                                                                        page: EditRequirementPage):

        # Initialize connected_listbox and connections list with sample data for tests purposes
        page.connected_listbox = ttk.Treeview(app)

        # Simulate drag and drop events in the traceability tab
        page.on_drag(tk.Event())
        page.on_drop(tk.Event())

        # Assert that the connections list is updated correctly
        assert len(page.connections) == 1

    #  Handles non-existent requirement in requirement_list in edit method
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_non_existent_requirement_in_requirement_list_in_edit_method(self, app: MockMainApplication,
                                                                                 page: EditRequirementPage):
        non_existent_id = -1  # Assuming -1 is not a valid ID in requirement_list
        with pytest.raises(KeyError):
            requirement_list.update(non_existent_id, "Section", "Subsection", "Title", "Text", ["Tag"])

    #  Handles requirement with missing attributes in on_show
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_requirement_with_missing_attributes_in_on_show(self, app: MockMainApplication,
                                                                    page: EditRequirementPage):
        incomplete_requirement = Requirement(None, None, None, None, [])
        incomplete_requirement.unique_id = 999  # Assign a unique ID for tests
        requirement_list.append(incomplete_requirement)

        page.requirement = incomplete_requirement

        # Initialize fields that will be populated by on_show
        page.title_entry = tk.Entry(app)
        page.section = tk.StringVar()
        page.subsection = tk.StringVar()
        page.requirement_text = tk.Text(app)

        # Call on_show and check if it handles missing attributes gracefully
        try:
            page.on_show()
            assert True  # If no exception is raised, the test passes
            assert not page.title_entry.get()  # Should be empty since title is None
            assert not page.section.get()  # Should be empty since section is None
            assert not page.subsection.get()  # Should be empty since subsection is None
            assert not page.requirement_text.get("1.0", tk.END).strip()  # Should be empty since text is None
            assert not list(page.tagging_text.get(0, tk.END))  # Should be empty since tags are None
        except Exception as e:
            pytest.fail(f"on_show raised an exception with missing attributes: {e}")

    #  Handles empty or invalid input fields in submit_requirement
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_empty_or_invalid_input_fields_in_submit_requirement(self, app: MockMainApplication,
                                                                         page: EditRequirementPage):

        # Create entries with empty or invalid data
        page.entries = {
            "section": tk.Entry(app),
            "subsection": tk.Entry(app),
            "title": tk.Entry(app),
            "text": tk.Entry(app),
            "tags": tk.Entry(app)
        }

        # Leave all fields empty and call submit_requirement
        try:
            page.add()
            # Check if a new requirement was added despite empty fields (it shouldn't be added)
            assert len(page.connections) == 0

            # Now insert invalid data and call submit_requirement again
            page.entries["tags"].insert(0, "InvalidTagFormat")
            page.add()

            # Check if a new requirement was added despite invalid tags (it shouldn't be added)
            assert len(page.connections) == 0

            # If no exception is raised and no new requirement is added, the test passes
            assert True

        except Exception as e:
            pytest.fail(f"submit_requirement raised an exception with empty or invalid input fields: {e}")

    #  Handles empty connections list in update_listbox
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_empty_connections_list_in_update_listbox(self, app: MockMainApplication,
                                                              page: EditRequirementPage):
        # Initialize connected_listbox and connections list as empty
        page.connected_listbox = ttk.Treeview(app)

        # Call update_listbox with empty connections list and check if it handles gracefully
        try:
            page.update_listbox()

            # Check if connected_listbox remains empty after update_listbox call
            assert len(page.connected_listbox.get_children()) == 0

            # If no exception is raised and connected_listbox remains empty, the test passes
            assert True

        except Exception as e:
            pytest.fail(f"update_listbox raised an exception with empty connections list: {e}")

    #  Handles selection events in the traceability tab
    @pytest.mark.parametrize('edit_requirement_page', [req_complete], indirect=True)
    def test_handles_selection_events_in_traceability_tab(self, app: MockMainApplication, page: EditRequirementPage):

        # Simulate selection event in connectable listbox
        event = tk.Event()
        event.widget = page.connectable_listbox

        try:
            page.on_select(event)
            assert True  # If no exception is raised, the test passes

        except Exception as e:
            pytest.fail(f"on_select raised an exception during selection event handling in traceability tab: {e}")
