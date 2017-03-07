""" Functional tests for the Obey simple list app """

from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """ Tests of item validation and submission """

    def test_cannot_add_empty_item(self):
        """ An empty list item doesn't save, it prompts """

        # ryan goes to the site and gets confused and presses enter
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # the page refreshes and he gets usage guidance, e.g. fill in
        # the form, sweetie

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            "You can't add an empty item!"
        ))

        # he adds an item about something cute, it works
        self._type_and_submit_item('Buy Jason a Photo')
        self._wait_for_row_in_list_table('1: Buy Jason a Photo')

        # cat hits enter again...cause ugh cat.
        self.get_item_input_box().send_keys(Keys.ENTER)

        # same error! wow!

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has_error').text,
            "You can't add an empty item!"
        ))

        # he adds another item alright?
        self._type_and_submit_item('Buy a photo frame')
        self._wait_for_row_in_list_table('1: Buy Jason a Photo')
        self._wait_for_row_in_list_table('2: Buy a photo frame')
