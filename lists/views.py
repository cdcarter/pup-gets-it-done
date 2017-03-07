""" Lists app views
"""
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.forms import ItemForm
from lists.models import Item, List


def home_page(request):
    """ The home_page view, which invites a user to engage """

    return render(request, 'home.html',  {'form': ItemForm()})


def view_list(request, list_id):
    """ handle requests for the lists resource """
    list_ = List.objects.get(id=list_id)

    if request.method == 'POST':
        try:
            item = Item.objects.create(text=request.POST['text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
            return render(request, 'home.html', {'error': error})
        
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list': list_, 'form': ItemForm()})


def new_list(request):
    """ Create a new list w/ an item """

    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(list_)



def add_item(request, list_id):
    """ Add an item to an existing list """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_)
    redirect(list_)
