import logging
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch

import pytest

from src.UI.pages import requirements
from src.UI.pages.paging_handle import PagesEnum
import src.UI.pages.paging_handle as PagingHandle
from src.UI.pages.requirements import AddRequirementPage
from src.structures.lists import requirement_list
from src.structures.records import Code, Requirement
from src.structures.records.record import Record

from tests.fixtures.app_fixtures import app
from tests.fixtures.page_fixtures import add_requirement_page
from tests.mocks.mock_main_app import MockMainApplication
from tests.utils.decorators import main_app_test

# Set up logging to output to the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class TestAddRequirementPage:
    """
    TestAddRequirementPage

    This class contains test cases for the AddRequirementPage functionality. The tests cover
    various aspects of the page including initialization, adding requirements, and handling invalid inputs.

    Included Tests:
    ---------------

    1. test_initialization
       - Summary: Verifies that the AddRequirementPage initializes correctly with all required components.

    2. test_add_requirement
       - Summary: Tests the functionality of adding a new requirement to ensure it is correctly processed and displayed.

    3. test_invalid_input
       - Summary: Ensures that invalid input is properly handled and appropriate error messages are displayed.

    4. test_clear_form
       - Summary: Checks if the form fields are correctly cleared after adding a requirement or pressing the clear button.

    5. test_form_validation
       - Summary: Validates that the form input fields meet the required validation rules before submission.

    6. test_submit_button_enabled
       - Summary: Tests that the submit button is only enabled when all required fields are correctly filled.

    7. test_cancel_button
       - Summary: Ensures that pressing the cancel button correctly discards the form input and navigates back to the previous page.

    8. test_prepopulate_fields
       - Summary: Verifies that the fields are correctly prepopulated when editing an existing requirement.

    9. test_error_handling
       - Summary: Checks the error handling mechanism when the form submission fails due to server errors.

   """

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        Record.clear_records()
        requirement_list.clear()

    def check_components(self, page):
        # Access the notebook widget
        notebook = page.nametowidget('add_requirement_body')
        assert isinstance(notebook, ttk.Notebook)

        # Verify the notebook has two tabs
        assert notebook.index("end") == 2

        # Verify the text of the tabs
        assert notebook.tab(0, "text") == "Add Requirement"
        assert notebook.tab(1, "text") == "Traceability"

        # Access the tabs by name
        requirement_tab = notebook.nametowidget('add_requirements_req_tab')
        traceability_tab = notebook.nametowidget('add_requirements_trace_tab')
        assert requirement_tab.winfo_ismapped() or traceability_tab.winfo_ismapped()
        # Verify the components in the requirement tab
        if requirement_tab.winfo_ismapped():
            assert page.title_label.winfo_ismapped()
            assert page.section_label.winfo_ismapped()
            assert page.subsection_label.winfo_ismapped()
            assert page.tagging_label.winfo_ismapped()
            assert page.requirement_label.winfo_ismapped()
            assert page.title_entry.winfo_ismapped()
            assert page.section.winfo_ismapped()
            assert page.subsection.winfo_ismapped()
            assert page.tagging_text.winfo_ismapped()
            assert page.requirement_text.winfo_ismapped()

        # Verify the components in the traceability tab
        if traceability_tab.winfo_ismapped():
            assert page.connectable_listbox.winfo_ismapped()
            assert page.connected_listbox.winfo_ismapped()

    def test_all_components_initialization_and_locations(self, app: MockMainApplication,
                                                         add_requirement_page: AddRequirementPage):
        """
        Test: Verify that all UI components are properly initialized and located.
        """

        # Adding a slight delay to ensure the UI components are fully rendered
        app.after(500, self.check_components, add_requirement_page)

    def test_switching_tabs(self, app: MockMainApplication,
                            add_requirement_page: AddRequirementPage):
        """
        Test: Verify that switching between tabs works correctly.
        """
        # Access the notebook widget
        notebook = add_requirement_page.nametowidget('add_requirement_body')
        assert isinstance(notebook, ttk.Notebook)

        # Access the tabs by name
        requirement_tab = notebook.nametowidget('add_requirements_req_tab')
        traceability_tab = notebook.nametowidget('add_requirements_trace_tab')

        # Switch to the Traceability tab
        notebook.select(traceability_tab)
        app.update()  # Ensure the GUI updates the tab selection

        # Adding a slight delay to ensure the UI components are fully rendered
        app.after(500, self.check_components, add_requirement_page, notebook)

        # Switch back to the Add Requirement tab
        notebook.select(requirement_tab)
        app.update()  # Ensure the GUI updates the tab selection
        # Adding a slight delay to ensure the UI components are fully rendered
        app.after(500, self.check_components, add_requirement_page, notebook)

    def test_adds_code_items_to_treeview_under_implementations(self, app: MockMainApplication,
                                                               add_requirement_page: AddRequirementPage):
        """
        Test: Successfully adds Code items to the treeview under 'Implementations'.
        """
        treeview = ttk.Treeview(app)
        connected_items = [Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True)]
        page = requirements.AddRequirementPage(app)
        page._add_lists_to_treeview(connected_items, treeview)
        assert treeview.get_children() == ('I001',)
        assert treeview.item('I001', 'text') == 'Implementations'
        assert treeview.get_children('I001') == ('Code-0',)

    def test_adds_requirement_items_to_treeview_under_related_requirements(self, app: MockMainApplication,
                                                                           add_requirement_page: AddRequirementPage):
        """
        Test: Successfully adds Requirement items to the treeview under 'Related Requirements'.
        """
        treeview = ttk.Treeview(app)
        connected_items = [Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert treeview.get_children() == ('I001',)
        assert treeview.item('I001', 'text') == 'Related Requirements'
        assert treeview.get_children('I001') == ('Req-section1-subsection1-0',)

    def test_handles_mixed_lists_of_code_and_requirement_items(self, app: MockMainApplication,
                                                               add_requirement_page: AddRequirementPage):
        """
        Test: Handles mixed lists of Code and Requirement items correctly.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"])
        ]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2
        assert treeview.item(treeview.get_children()[0], 'text') == 'Related Requirements'
        assert treeview.item(treeview.get_children()[1], 'text') == 'Implementations'

    def test_maintains_order_of_items_as_per_input_list(self, app: MockMainApplication,
                                                        add_requirement_page: AddRequirementPage):
        """
        Test: Maintains the order of items as per the input list.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"]),
            Code("file2", "private", "Class2", "method2", ["arg3", "arg4"], 1, 21, False)
        ]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        children = treeview.get_children()
        assert len(children) == 2
        assert treeview.item(children[0], 'text') == 'Related Requirements'
        assert treeview.item(children[1], 'text') == 'Implementations'

    def test_handles_empty_list_without_errors(self, app: MockMainApplication,
                                               add_requirement_page: AddRequirementPage):
        """
        Test: Handles empty lists without errors.
        """
        treeview = ttk.Treeview(app)
        connected_items = []
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 0

    def test_manages_lists_with_only_code_items(self, app: MockMainApplication,
                                                add_requirement_page: AddRequirementPage):
        """
        Test: Manages lists with only Code items.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
        ]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 1
        assert treeview.item(treeview.get_children()[0], 'text') == 'Implementations'

    def test_handles_missing_or_none_unique_ids(self, app: MockMainApplication,
                                                add_requirement_page: AddRequirementPage):
        """
        Test: Handles missing or None unique IDs gracefully.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Code("file1", "public", "Class1", "method1", ["arg1", "arg2"], 1, 21, True),
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"], new_unique_id=None)
        ]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2

    def test_logs_errors_when_insertion_fails(self, app: MockMainApplication,
                                              add_requirement_page: AddRequirementPage):
        """
        Test: Logs errors when insertion into the treeview fails.
        """
        treeview = ttk.Treeview(app)

        class FaultyCode(Code):
            @property
            def unique_id(self):
                raise ValueError("Faulty ID")

        connected_items = [FaultyCode("file3", "protected", "Class3", "method3", ["arg5"], 1, 21, True)]

        with pytest.raises(ValueError):
            add_requirement_page._add_lists_to_treeview(connected_items, treeview)

    def test_handles_faulty_code_items_that_raise_exceptions(self, app: MockMainApplication,
                                                             add_requirement_page: AddRequirementPage):
        """
        Test: Handles faulty Code items that raise exceptions gracefully.
        """
        treeview = ttk.Treeview(app)

        class FaultyCode(Code):
            @property
            def unique_id(self):
                raise ValueError("Faulty ID")

        connected_items = [FaultyCode("file3", "protected", "Class3", "method3", ["arg5"], 1, 21, True)]

        with pytest.raises(ValueError):
            add_requirement_page._add_lists_to_treeview(connected_items, treeview)

    def test_handles_drag_and_drop_events_with_invalid_data(self, app: MockMainApplication,
                                                            add_requirement_page: AddRequirementPage):
        """
        Test: Handles drag and drop events with invalid data gracefully.
        """

        class MockEvent(tk.Event):
            def __init__(self, widget, x_root, y_root):
                self.widget = widget
                self.x_root = x_root
                self.y_root = y_root

            @property
            def x(self):
                return self.x_root

            @property
            def y(self):
                return self.y_root

        mock_widget = tk.Label(app, text='mock_widget')
        mock_widget._drag_data = None  # Invalid data

        event = MockEvent(mock_widget, 100, 100)

        add_requirement_page.on_drop(event)  # Should handle gracefully without errors

    def test_manages_lists_with_only_requirement_items(self, app: MockMainApplication,
                                                       add_requirement_page: AddRequirementPage):
        """
        Test: Manages lists with only Requirement items.
        """
        treeview = ttk.Treeview(app)
        connected_items = [
            Requirement("section1", "subsection1", "Title1", "Text1", ["tag1"]),
            Requirement("section2", "subsection2", "Title2", "Text2", ["tag2"])
        ]
        add_requirement_page._add_lists_to_treeview(connected_items, treeview)
        assert len(treeview.get_children()) == 2
        assert treeview.item(treeview.get_children()[0], 'text') == 'Related Requirements'

    def test_handles_large_lists_efficiently(self, app: MockMainApplication,
                                             add_requirement_page: AddRequirementPage):
        """
        Test: Handles large lists efficiently.
        """
        treeview = ttk.Treeview(app)

        connected_items = [
            Code(f"file{i}", f"access{i}", f"Class{i}", f"method{i}", [f"arg{i}"], i, i + 1, True) for i
            in range(1000)]

        import time
        start_time = time.time()

        add_requirement_page._add_lists_to_treeview(connected_items, treeview)

        end_time = time.time()

        assert (end_time - start_time) < 5  # Ensure it runs within 5 seconds for 1000 items

    def test_ui_component_initialization(self, app: MockMainApplication,
                                         add_requirement_page: AddRequirementPage):
        """
        Test: Verify that all UI components are properly initialized and visible.
        """
        assert add_requirement_page.title_label.cget("text") == "Title:"
        assert add_requirement_page.section_label.cget("text") == "Section:"
        assert add_requirement_page.subsection_label.cget("text") == "Subsection:"
        assert add_requirement_page.tagging_label.cget("text") == "Tags:"
        assert add_requirement_page.requirement_label.cget("text") == "Requirement:"

    def test_requirement_addition(self, app: MockMainApplication,
                                  add_requirement_page: AddRequirementPage):
        """
        Test: Verify that a requirement is correctly added to the requirement list.
        """
        add_requirement_page.title_entry.insert(0, "Test Requirement")
        add_requirement_page.section.variable = "Test Section"
        add_requirement_page.subsection.variable = "Test Subsection"
        add_requirement_page.requirement_text.insert("1.0", "This is a test requirement.")
        add_requirement_page.tagging_text.list = ["tag1", "tag2"]

        add_requirement_page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == "Test Requirement"
        assert added_req.section == "Test Section"
        assert added_req.sub == "Test Subsection"
        assert added_req.text == "This is a test requirement."
        assert added_req.tags == ["tag1", "tag2"]

    def test_cancel_operation(self, app: MockMainApplication,
                              add_requirement_page: AddRequirementPage):
        """
        Test: Verify that the cancel operation navigates back to the previous page.
        """
        with patch('src.UI.pages.paging_handle.page_return', autospec=True) as mock_page_return:
            add_requirement_page.cancel()
            mock_page_return.assert_called_once()

    def test_section_and_subsection_updates(self, app: MockMainApplication,
                                            add_requirement_page: AddRequirementPage):
        """
        Test: Verify that selecting a section updates the subsection combobox correctly.
        """
        add_requirement_page.section.variable = "Section 1"
        requirement_list.append(Requirement("Section 1", "Subsection 1.1", "", "", []))
        requirement_list.append(Requirement("Section 1", "Subsection 1.2", "", "", []))
        add_requirement_page.update_combobox_b()
        assert "Subsection 1.1" in add_requirement_page.subsection.cget("values")
        assert "Subsection 1.2" in add_requirement_page.subsection.cget("values")

    def test_drag_and_drop_functionality(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify the drag and drop functionality with valid and invalid data.
        """

        # Assuming `page` is an instance of `AddRequirementPage`
        notebook = add_requirement_page.notebook  # Assuming your notebook is assigned to `page.notebook`

        # Switch to the "Trace" tab
        trace_tab_index = notebook.nametowidget('add_requirements_trace_tab') # If tabs are named, use the name here
        notebook.select(trace_tab_index)
        app.update_idletasks()
        add_requirement_page.connections = []  # Ensure connections is initialized
        # Simulate a valid drag and drop operation
        add_requirement_page.connectable_listbox.insert("", "end", iid="item1", text="Item 1")
        add_requirement_page.connectable_listbox.selection_set("item1")

        valid_event = tk.Event()
        valid_event.widget = add_requirement_page.connectable_listbox
        valid_event.x_root = add_requirement_page.connectable_listbox.winfo_rootx() + 10
        valid_event.y_root = add_requirement_page.connectable_listbox.winfo_rooty() + 10

        add_requirement_page.on_drag(valid_event)

        valid_event.widget = add_requirement_page.connected_listbox
        valid_event.x_root = add_requirement_page.connected_listbox.winfo_rootx() + 10
        valid_event.y_root = add_requirement_page.connected_listbox.winfo_rooty() + 10

        add_requirement_page.on_drop(valid_event)
        app.update_idletasks()
        assert len(add_requirement_page.connections) > 0
        # Simulate an invalid drag and drop operation
        invalid_event = tk.Event()
        invalid_event.widget = add_requirement_page.connectable_listbox
        invalid_event.x_root = add_requirement_page.connectable_listbox.winfo_rootx() + 10
        invalid_event.y_root = add_requirement_page.connectable_listbox.winfo_rooty() + 10

        add_requirement_page.on_drag(invalid_event)

        invalid_event.widget = add_requirement_page.connected_listbox
        invalid_event.x_root = add_requirement_page.connected_listbox.winfo_rootx() + 10
        invalid_event.y_root = add_requirement_page.connected_listbox.winfo_rooty() + 10

        add_requirement_page.on_drop(invalid_event)
        assert len(add_requirement_page.connections) > 0  # Should handle gracefully without errors

    def test_ui_layout_and_resizing(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
         Test: Ensure the layout adjusts correctly when the window is resized.
         """
        # Set initial geometry and update the UI
        print(f"Initial size: {app.winfo_width()}x{app.winfo_height()}")
        app.geometry("800x600")
        app.update()
        print(f"Resized size: {app.winfo_width()}x{app.winfo_height()}")
        initial_height = add_requirement_page.requirement_text.winfo_height()
        initial_width = add_requirement_page.requirement_text.winfo_width()

        # Scenario 1: Resize to a smaller window
        app.geometry("600x400")
        app.update()
        resized_height_small = add_requirement_page.requirement_text.winfo_height()
        resized_width_small = add_requirement_page.requirement_text.winfo_width()

        assert resized_height_small < initial_height, f"Height did not decrease: {resized_height_small} >= {initial_height}"
        assert resized_width_small < initial_width, f"Width did not decrease: {resized_width_small} >= {initial_width}"

        # Scenario 2: Resize to a larger window
        app.geometry("1000x800")
        app.update()
        resized_height_large = add_requirement_page.requirement_text.winfo_height()
        resized_width_large = add_requirement_page.requirement_text.winfo_width()

        assert resized_height_large > resized_height_small, f"Height did not increase: {resized_height_large} <= {resized_height_small}"
        assert resized_width_large > resized_width_small, f"Width did not increase: {resized_width_large} <= {resized_width_small}"

        # Scenario 3: Resize to a very small window (edge case)
        app.geometry("200x150")
        app.update()
        resized_height_edge = add_requirement_page.requirement_text.winfo_height()
        resized_width_edge = add_requirement_page.requirement_text.winfo_width()

        assert resized_height_edge < resized_height_small, f"Height did not decrease significantly: {resized_height_edge} >= {resized_height_small}"
        assert resized_width_edge < resized_width_small, f"Width did not decrease significantly: {resized_width_edge} >= {resized_width_small}"

        # Scenario 4: Resize back to the initial size
        app.geometry("800x600")
        app.update()
        resized_height_back = add_requirement_page.requirement_text.winfo_height()
        resized_width_back = add_requirement_page.requirement_text.winfo_width()

        assert abs(
            resized_height_back - initial_height) <= 2, f"Height did not return close to initial: {resized_height_back} != {initial_height}"
        assert abs(
            resized_width_back - initial_width) <= 2, f"Width did not return close to initial: {resized_width_back} != {initial_width}"

    def test_add_empty_requirement(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify that adding an empty requirement shows an error or does not add.
        """
        add_requirement_page.add()
        assert len(requirement_list.get_requirement_list()) == 0  # Assuming the list should remain empty

    def test_add_duplicate_requirement(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify that adding duplicate requirements is handled correctly.
        """
        add_requirement_page.title_entry.insert(0, "Test Requirement")
        add_requirement_page.section.variable = "Test Section"
        add_requirement_page.subsection.variable = "Test Subsection"
        add_requirement_page.requirement_text.insert("1.0", "This is a test requirement.")
        add_requirement_page.tagging_text.list = ["tag1", "tag2"]

        add_requirement_page.add()
        add_requirement_page.add()  # Attempt to add the same requirement again

        assert len(requirement_list.get_requirement_list()) == 1  # Should not add duplicate

    def test_add_requirement_with_max_length_values(self, app: MockMainApplication,
                                                    add_requirement_page: AddRequirementPage):
        """
        Test: Verify adding a requirement with maximum length values for fields.
        """
        long_text = "a" * 1000
        add_requirement_page.title_entry.insert(0, long_text)
        add_requirement_page.section.variable = long_text
        add_requirement_page.subsection.variable = long_text
        add_requirement_page.requirement_text.insert("1.0", long_text)
        add_requirement_page.tagging_text.list = [long_text]

        add_requirement_page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == long_text
        assert added_req.section == long_text
        assert added_req.sub == long_text
        assert added_req.text == long_text
        assert added_req.tags == [long_text]

    def test_add_requirement_with_special_characters(self, app: MockMainApplication,
                                                     add_requirement_page: AddRequirementPage):
        """
        Test: Verify adding a requirement with special characters in fields.
        """
        special_text = "!@#$%^&*()_+"
        add_requirement_page.title_entry.insert(0, special_text)
        add_requirement_page.section.variable = special_text
        add_requirement_page.subsection.variable = special_text
        add_requirement_page.requirement_text.insert("1.0", special_text)
        add_requirement_page.tagging_text.list = [special_text]

        add_requirement_page.add()

        added_req = requirement_list.get_requirement_list()[-1]
        assert added_req.title == special_text
        assert added_req.section == special_text
        assert added_req.sub == special_text
        assert added_req.text == special_text
        assert added_req.tags == [special_text]

    def test_error_handling_on_invalid_data(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify error handling when invalid data is provided.
        """
        # Simulate invalid data scenario
        with patch('src.structures.lists.requirement_list.append', side_effect=Exception("Test Error")):
            add_requirement_page.add()
            # Verify that the error was logged or handled gracefully
            # Adjust this assertion based on your error handling implementation
            assert len(requirement_list.get_requirement_list()) == 0

    def test_state_persistence_on_navigation(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify state persistence when navigating between pages.
        """
        add_requirement_page.title_entry.insert(0, "Persistent Requirement")
        add_requirement_page.section.variable = "Persistent Section"
        add_requirement_page.subsection.variable = "Persistent Subsection"
        add_requirement_page.requirement_text.insert("1.0", "Persistent text")
        add_requirement_page.tagging_text.list = ["persistent_tag"]

        # Simulate navigation
        PagingHandle.show_page(PagesEnum.RECORD_VIEW)
        PagingHandle.show_page(PagesEnum.ADD_REQUIREMENT)

        # Verify state persistence
        assert add_requirement_page.title_entry.get() == "Persistent Requirement"
        assert add_requirement_page.section.variable == "Persistent Section"
        assert add_requirement_page.subsection.variable == "Persistent Subsection"
        assert add_requirement_page.requirement_text.get("1.0", "end-1c") == "Persistent text"
        assert add_requirement_page.tagging_text.list == ["persistent_tag"]

    def test_component_visibility_based_on_input(self, app: MockMainApplication,
                                                 add_requirement_page: AddRequirementPage):
        """
        Test: Verify the visibility of components based on certain inputs.
        """
        add_requirement_page.section.variable = "Some Section"
        requirement_list.append(Requirement("Some Section", "Subsection 1", "", "", []))
        add_requirement_page.update_combobox_b()

        # Verify that subsection is updated and visible
        # Subsection defaults to "", then selection happens by user.
        assert add_requirement_page.subsection.variable == ""
        assert add_requirement_page.subsection.winfo_ismapped()

    def test_event_triggered_actions(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify that correct actions are triggered on various UI events.
        """
        # Simulate button click event
        add_requirement_page.add_button.invoke()
        assert len(requirement_list.get_requirement_list()) == 0  # Assuming no valid data to add

        add_requirement_page.cancel_button.invoke()
        # Assuming paging_handle.page_return() should be called
        with patch('src.UI.pages.paging_handle.page_return', autospec=True) as mock_page_return:
            add_requirement_page.cancel()
            mock_page_return.assert_called_once()

    def test_combobox_options_update(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify that the ComboboxWithAdd options are correctly updated when the update_combobox_b method is triggered by a section change.
        """
        section_options = ["Section 1", "Section 2"]
        add_requirement_page.section.set_options(section_options)
        add_requirement_page.section.variable = "Section 1"

        requirement_list.append(Requirement("Section 1", "Subsection 1.1", "", "", []))
        requirement_list.append(Requirement("Section 1", "Subsection 1.2", "", "", []))
        add_requirement_page.update_combobox_b()

        assert "Subsection 1.1" in add_requirement_page.subsection.cget("values")
        assert "Subsection 1.2" in add_requirement_page.subsection.cget("values")

    def test_update_combobox_b_with_invalid_section(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify the behavior when an invalid section is selected.
        """
        add_requirement_page.section.variable = "Invalid Section"
        add_requirement_page.update_combobox_b()
        assert add_requirement_page.subsection.cget("values") == ('',)

    def test_ui_state_reset_on_reload(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        """
        Test: Verify that the UI components are reset correctly when the page is reloaded.
        """
        add_requirement_page.title_entry.insert(0, "Persistent Requirement")
        add_requirement_page.section.variable = "Persistent Section"
        add_requirement_page.subsection.variable = "Persistent Subsection"
        add_requirement_page.requirement_text.insert("1.0", "Persistent text")
        add_requirement_page.tagging_text.list = ["persistent_tag"]

        # Simulate page reload
        add_requirement_page.create_body()
        app.update()  # Ensure all widgets are updated

        # Verify state reset
        assert add_requirement_page.title_entry.get() == ""
        assert add_requirement_page.section.variable == ""
        assert add_requirement_page.subsection.variable == ""
        assert add_requirement_page.requirement_text.get("1.0", "end-1c") == ""
        assert add_requirement_page.tagging_text.list == []

    def test_display_tree(self, app: MockMainApplication, add_requirement_page: AddRequirementPage):
        assert add_requirement_page.winfo_ismapped() == 1