from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):
    """ Unit Tests for the home_page view
    """
    def test_root_url_home_page(self):
        """ the root URL should resolve to the home_page view """
        found = resolve('/')
        self.assertEqual(found.func, home_page)


