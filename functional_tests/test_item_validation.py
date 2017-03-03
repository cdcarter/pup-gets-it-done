""" Functional tests for the Obey simple list app """

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """ Tests of item validation and submission """

    def test_cannot_add_empty_item(self):
        """ An empty list item doesn't save, it prompts """

        # ryan goes to the site and gets confused and presses enter

        # the page refreshes and he gets usage guidance, e.g. fill in
        # the form, sweetie

        # he adds an item about something cute, it works

        # cat hits enter again...cause ugh cat.

        # same error! wow!

        self.fail('write the test, pup')
