""" Lists app views
"""
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    """ The home_page view, which invites a user to engage """

    return render(request, 'home.html')


def view_list(request, list_id):
    """ handle requests for the lists resource """
    list_ = List.objects.get(id=list_id)

    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """ Create a new list w/ an item """

    list_ = List.objects.create()
    Item.objects.create(
        text=request.POST.get('item_text', ''),
        list=list_
    )
    return redirect(f'/lists/{list_.id}/')


def add_item(request, list_id):
    """ Add an item to an existing list """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_id}/')
