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

    def test_home_page_renders_todo_home(self):
        """ The home_page view should be a todo list home """
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertTrue(html.startsWith('<html>'))
        self.assertIn('<title>To-do List</title>',html)
