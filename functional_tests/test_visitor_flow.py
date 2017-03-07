""" Functional tests for the Obey simple list app """
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    """ A Simple Visitor Test Flow """

    def test_start_list_one_user(self):
        """ Jason, a power user, can start a list """

        self.browser.get(self.server_url)

        # He sees that it's a todolist app! :eyeroll:
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is offered to enter a todo
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do'
        )
        # He types "Pick out a present for pup" into the box
        # When he hits update, the page updates, and now the page
        # lists "1: Pick out a present for pup"
        self._type_and_submit_item('Pick out a present for pup')
        self._wait_for_row_in_list_table('1: Pick out a present for pup')

        # There is still a text box for adding another item
        # He enters "Order present for pup"
        self._type_and_submit_item('Order present for pup')

        # The page updates again and shows two items on the list
        self._wait_for_row_in_list_table('1: Pick out a present for pup')
        self._wait_for_row_in_list_table('2: Order present for pup')

    def test_many_users_many_urls(self):
        """ Multiple users start lists at different urls. """

        self.browser.get(self.server_url)
        self._type_and_submit_item('Pick out a present for pup')
        self._wait_for_row_in_list_table('1: Pick out a present for pup')

        jason_list_url = self.browser.current_url
        self.assertRegex(jason_list_url, '/lists/.+')

        # a new user, christian, comes to the site!

        self.browser.quit()
        self.setUp()
        self.browser.get(self.server_url)

        # he doesn't see jasons list, thank goodness!
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Pick out a present for pup', page_text)
        self.assertNotIn('Order present', page_text)

        # he starts his own, much more boring, list
        self._type_and_submit_item('Learn python')
        self._wait_for_row_in_list_table('1: Learn python')

        christian_list_url = self.browser.current_url
        self.assertRegex(christian_list_url, '/lists/.+')
        self.assertNotEqual(christian_list_url, jason_list_url)

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('for pup', page_text)
