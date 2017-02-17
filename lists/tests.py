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

    def test_home_page_loads_mutiple_items(self):
        """ The home page table renders a row for each item """
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

    def test_save_post_requests(self):
        """ The / endpoint creates a new todo on POST """
        self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual('A new list item', new_item.text)

    def test_redirect_after_post(self):
        """ / endpoint redirects back to / on POST """
        response = self.client.post('/', data={'item_text': 'A new list item'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_dont_save_get_request(self):
        """ Test that no items are created on a GET """
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

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
