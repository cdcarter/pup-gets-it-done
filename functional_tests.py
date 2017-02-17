""" Functional tests for the Obey simple list app """

import unittest

from selenium import webdriver

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

        # He is offered to enter a todo
        self.fail('Finish writing the test, dude!')
        # He types "Pick out a present for pup" into the box

        # When he hits update, the page updates, and now the page
        # lists "1: Pick out a present for pup"

        # There is still a text box for adding another item

        # He enters "Order present for pup"

        # The page updates again and shows two items on the list

        # Jason can copy the link at the bottom of the page for this list.

        # Jason opens that link up

        # The todo list is there.

if __name__ == '__main__':
    unittest.main()
    