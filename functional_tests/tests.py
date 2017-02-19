""" Functional tests for the Obey simple list app """
import time
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """ A Simple Visitor Test Flow """
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def _wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as ex:
                if time.time() - start_time > MAX_WAIT:
                    raise ex
                time.sleep(0.1)

    def _type_and_submit_item(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def test_start_list_one_user(self):
        """ Jason, a power user, can start a list """

        self.browser.get(self.live_server_url)

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

        self.browser.get(self.live_server_url)
        self._type_and_submit_item('Pick out a present for pup')
        self._wait_for_row_in_list_table('1: Pick out a present for pup')

        jason_list_url = self.browser.current_url
        self.assertRegex(jason_list_url, '/lists/.+')

        # a new user, christian, comes to the site!

        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

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
        