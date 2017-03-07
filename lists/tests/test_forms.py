""" Tests for the Forms in the lists app. """

from django.test import TestCase
from lists.forms import EMPTY_ITEM_ERROR, ItemForm

class ItemFormTest(TestCase):
    """ Tests of the Item Form """

    def test_form_renders_item_text_input(self):   # pylint: disable=C0103
        """ Item is a text input. """
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_empty_item(self):  # pylint: disable=C0103
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertIn(EMPTY_ITEM_ERROR, form.errors['text'])