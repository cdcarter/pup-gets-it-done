""" Lists app views
"""
from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    """ The home_page view, which invites a user to engage """
    return HttpResponse('<html><title>To-Do List</title></html>')
