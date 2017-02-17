""" Unit tests for the lists app """

from django.test import TestCase

class HomePageTest(TestCase):
    """ Unit Tests for the home_page view
    """
    def test_home_page_is_todo_home(self):
        """ The / endpoint should be a todo list home """
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_handle_POST_request(self):
        """ The / endpoint allows POST with a new todo """
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        