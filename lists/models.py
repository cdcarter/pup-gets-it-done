""" Django ORM models for the Lists app """

from django.db import models

class Item(models.Model):
    """ An item is a single todo item in the database """
    text = models.TextField(default='')
