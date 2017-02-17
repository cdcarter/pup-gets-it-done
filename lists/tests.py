""" Unit tests for the lists app """

from django.test import TestCase

class HomePageTest(TestCase):
    """ Unit Tests for the home_page view
    """
    def test_home_page_is_todo_home(self):
        """ The / endpoint should be a todo list home """
        response = self.client.get('/')

        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do List</title>', html)

        self.assertTemplateUsed(response, 'home.html')
