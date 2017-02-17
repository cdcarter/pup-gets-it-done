""" Functional tests for the Obey simple list app """
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(unittest.TestCase):
    """ A Simple Visitor Test Flow """
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_retrieve_list(self):
        """ Jason, a power user, can start a list
        and share it with a friend """

        self.browser.get('http://localhost:8000')

        # He sees that it's a todolist app! :eyeroll:
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is offered to enter a todo
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do'
        )
        # He types "Pick out a present for pup" into the box
        inputbox.send_keys('Pick out a present for pup')

        # When he hits update, the page updates, and now the page
        # lists "1: Pick out a present for pup"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '1: Pick out a present for pup',
            [row.text for row in rows]
        )

        # There is still a text box for adding another item
        inputbox = self.browser.find_element_by_id('id_new_item')

        # He enters "Order present for pup"
        inputbox.send_keys('Order present for pup')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and shows two items on the list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(
            '1: Pick out a present for pup',
            [row.text for row in rows]
        )
        self.assertIn(
            '2: Order present for pup',
            [row.text for row in rows]
        )

        # Jason can copy the link at the bottom of the page for this list.
        self.fail('finish tests')
        # Jason opens that link up

        # The todo list is there.

if __name__ == '__main__':
    unittest.main()
    