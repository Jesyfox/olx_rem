from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import View

from .models import Category, Item


class ShowCategory(View):
    def get(self, request, hierarchy=None):
        category_slug = hierarchy.split('/')
        parent = None
        root = Category.objects.all()
        for slug in category_slug[:-1]:
            parent = root.get(parent=parent, slug=slug)

        try:
            categories = Category.objects.get(parent=parent, slug=category_slug[-1])
        except Exception as e:
            print('Exception!: ', e)
            categories = get_object_or_404(Item, slug=category_slug[-1])
            return render(request, 'index.html', {'categories': categories})
        else:
            return render(request, 'categories.html', {'categories': categories})


class Index(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.categories = Category.objects.all()
        self.items = Item.objects.all()
        self.auth_form = AuthenticationForm
        self.context.update(categories=self.categories, items=self.items, form=self.auth_form)

    def get(self, request):
        return render(request, 'index.html', context=self.context)

    def post(self, request):
        auth_form = AuthenticationForm(request=request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            raw_password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'index.html', context=self.context)
        else:
            self.context.update(form=auth_form)
            return render(request, 'index.html', context=self.context)


def register(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            context = {'form': form}
            return render(request, 'index.html', context=context)
    elif request.method == 'GET':
        form = UserCreationForm()
        context.update(form=form)
        return render(request, 'index.html', context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

