""" Unit tests for the lists app models """

from django.test import TestCase
from lists.models import Item, List


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

    def test_get_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), '/lists/%d/' % (list_.id,))