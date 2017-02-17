""" Lists app views
"""
from django.shortcuts import render

def home_page(request):
    """ The home_page view, which invites a user to engage """
    return render(request, 'home.html')
