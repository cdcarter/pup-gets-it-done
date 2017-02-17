""" Unit tests for the lists app """

from django.test import TestCase
from lists.models import Item

class HomePageTest(TestCase):
    """ Unit Tests for the home_page view
    """
    def test_home_page_is_todo_home(self):
        """ The / endpoint should be a todo list home """
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_handle_post_request(self):
        """ The / endpoint allows POST with a new todo """
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
    """ Unit Tests for the Item ORM Model """
    def test_save_and_retrieve_items(self):
        """ Basic use of the DJango ORM """
        first_item = Item()
        first_item.text = 'The first item (ever) written'
        first_item.save()

        second_item = Item()
        second_item.text = 'the Second item written'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first item (ever) written')
        self.assertEqual(second_saved_item.text, second_item.text)
