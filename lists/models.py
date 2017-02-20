""" Django ORM models for the Lists app """

from django.db import models


class List(models.Model):
    """ A list of todos in the database """
    pass


class Item(models.Model):
    """ An item is a single todo item in the database """
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
