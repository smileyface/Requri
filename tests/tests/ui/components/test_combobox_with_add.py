from src.UI.components.combobox_with_add import ComboboxWithAdd  # Adjust the import path as needed
from tests.utils.decorators import tkinter_test
from tests.fixtures.root_fixture import root


class TestComboboxWithAdd:

    @tkinter_test
    def test_initialize_with_default_options(self, root):
        """
        Test: Initialize with default options and verify combobox values.
        """
        combobox = ComboboxWithAdd(root)
        assert combobox.combobox['values'] == ('',)  # Tkinter combobox returns an empty string for an empty list

    @tkinter_test
    def test_initialize_with_provided_options(self, root):
        """
        Test: Initialize with provided options and verify combobox values.
        """
        options = ['Option1', 'Option2']
        combobox = ComboboxWithAdd(root, options=options)
        assert combobox.combobox['values'] == ('', 'Option1', 'Option2')

    @tkinter_test
    def test_set_options_updates_combobox(self, root):
        """
        Test: Verify combobox updates correctly when set_options is called.
        """
        combobox = ComboboxWithAdd(root)
        new_options = ['NewOption1', 'NewOption2']
        combobox.set_options(new_options)
        assert combobox.combobox['values'] == ('', 'NewOption1', 'NewOption2')

    @tkinter_test
    def test_clear_combobox(self, root):
        """
        Test: Verify combobox clears correctly when clear is called.
        """
        options = ['Option1', 'Option2']
        combobox = ComboboxWithAdd(root, options=options)
        assert combobox.combobox['values'] == ('', 'Option1', 'Option2')
        combobox.clear()
        assert combobox.combobox['values'] == ('', )
        assert combobox.variable == ''

    @tkinter_test
    def test_selected_callback_triggered(self, root):
        """
        Test: Verify selected_callback is triggered on selection.
        """
        callback_triggered = False

        def callback(event):
            nonlocal callback_triggered
            callback_triggered = True

        options = ['Option1', 'Option2']
        combobox = ComboboxWithAdd(root, options=options, selected_callback=callback)
        combobox.combobox.set('Option1')
        combobox.combobox.event_generate("<<ComboboxSelected>>")
        assert callback_triggered

    @tkinter_test
    def test_update_displays_blank_value_at_top(self, root):
        """
        Test: Verify combobox displays blank value at the top after update.
        """
        options = ['Option1', 'Option2']
        combobox = ComboboxWithAdd(root, options=options)
        new_options = ['NewOption1', 'NewOption2']
        combobox.set_options(new_options)
        combobox.update()
        assert combobox.combobox['values'][0] == ''

    @tkinter_test
    def test_initialize_with_no_options(self, root):
        """
        Test: Initialize with no options and verify combobox values.
        """
        combobox = ComboboxWithAdd(root)
        assert combobox.combobox['values'] == ('', )  # Tkinter combobox returns an empty string for an empty list

    @tkinter_test
    def test_initialize_with_empty_options_list(self, root):
        """
        Test: Initialize with empty options list and verify combobox values.
        """
        combobox = ComboboxWithAdd(root, options=[])
        assert combobox.combobox['values'] == ('', )  # Tkinter combobox returns an empty string for an empty list

    @tkinter_test
    def test_set_options_with_empty_list(self, root):
        """
        Test: Verify behavior when set_options is called with an empty list.
        """
        combobox = ComboboxWithAdd(root)
        combobox.set_options([])
        assert combobox.combobox['values'] == ('',)

    @tkinter_test
    def test_clear_with_no_initial_options(self, root):
        """
        Test: Verify behavior when clear is called with no initial options.
        """
        combobox = ComboboxWithAdd(root)
        combobox.clear()
        assert combobox.combobox['values'] == ('',)
        assert combobox.variable == ''

    @tkinter_test
    def test_selected_callback_none(self, root):
        """
        Test: Verify behavior when selected_callback is None.
        """
        options = ['Option1', 'Option2']
        combobox = ComboboxWithAdd(root, options=options, selected_callback=None)
        combobox.combobox.set('Option1')
        # No assertion needed as we are just verifying no exception is raised
