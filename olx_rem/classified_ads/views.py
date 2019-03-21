from django.shortcuts import render, get_object_or_404

from .models import Category, Item


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    parent = None
    root = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(Item, slug=category_slug[-1])
        return render(request, "index.html", {'instance': instance})
    else:
        return render(request, 'categories.html', {'instance': instance})


def index(request):
    context = {}
    instance = Category.objects.all()
    items = Item.objects.all()

    context.update(instance=instance, items=items)
    return render(request, 'index.html', context=context)
