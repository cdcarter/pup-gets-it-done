""" Lists app views
"""
from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    """ The home_page view, which invites a user to engage """

    if request.method == 'POST':
        Item.objects.create(text=request.POST.get('item_text', ''))
        return redirect('/lists/the-only-list')

    return render(request, 'home.html')


def view_list(request):
    """ handle requests for the lists resource """

    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
