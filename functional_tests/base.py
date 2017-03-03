""" Functional tests for the Obey simple list app """
import sys
import time

from unittest import skip

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    """ Base case for lists app tests """

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

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
