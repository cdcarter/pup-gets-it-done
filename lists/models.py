""" Django ORM models for the Lists app """

from django.db import models
from django.core.urlresolvers import reverse


class List(models.Model):
    """ A list of todos in the database """

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    """ An item is a single todo item in the database """
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
