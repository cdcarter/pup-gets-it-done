""" Functional tests for the Obey simple list app """
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    """ Tests of the layout and styling of the lists app."""

    def test_layout_and_styling(self):
        """ The home page looks roughly what we expect it to """
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        self._type_and_submit_item('Learn python')
        self._wait_for_row_in_list_table('1: Learn python')

        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )


