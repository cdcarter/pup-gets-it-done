""" Unit tests for the lists app """

from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    """ Unit Tests for the home_page view
    """
    def test_home_page_is_todo_home(self):
        """ The / endpoint should be a todo list home """
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')


class ItemListModelTest(TestCase):
    """ Unit Tests for the Item ORM Model """
    def test_save_and_retrieve_items(self):
        """ Basic use of the DJango ORM """
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first item (ever) written'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'the Second item written'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(
            first_saved_item.text,
            'The first item (ever) written'
        )
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    """ Unit tests for the List view """

    def test_display_only_items_in_list(self):
        """ Getting a list should sho wonly objects in that list """
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_uses_list_template(self):
        """ Lists are rendered w/ the list template """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_save_post_requests(self):
        """ The /lists/new endpoint creates a new todo on POST """
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual('A new list item', new_item.text)

    def test_redirect_after_post(self):
        """ /lists/new endpoint redirects back to /the-only-list on POST """
        response = self.client.post(
            '/lists/new', data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_passes_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewItemTest(TestCase):
    """ Tests for the new Item view """

    def test_can_save_to_existing_list(self):
        """ POSTing /lists/id/add_item adds an item! """

        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        """ POSTing to /lists/id/add_item redirects to list view """
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
