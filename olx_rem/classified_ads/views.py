from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.views.generic import View

from .models import Category, Item


class BaseView(View):
    template_name = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.context = {}
        self.auth_form = AuthenticationForm()
        self.context.update(form=self.auth_form)

    def post(self, request, **kwargs):
        auth_form = AuthenticationForm(request=request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            raw_password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            self.context.update(form=auth_form)
            return render(request, self.template_name, context=self.context)


class ShowCategory(BaseView, View):
    template_name = 'categories.html'

    def get(self, request, hierarchy=None):
        category_slug = hierarchy.split('/')
        parent = None
        root = Category.objects.all()
        for slug in category_slug[:-1]:
            parent = root.get(parent=parent, slug=slug)

        try:
            categories = Category.objects.get(parent=parent, slug=category_slug[-1])
            self.context.update(categories=categories)
        except Exception as e:
            print('Exception!: ', e)
            categories = get_object_or_404(Item, slug=category_slug[-1])
            self.context.update(categories=categories)
            return render(request, 'index.html', self.context)
        else:
            return render(request, self.template_name, self.context)


class Index(BaseView, View):
    template_name = 'index.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories = Category.objects.all()
        self.items = Item.objects.all()
        self.context.update(categories=self.categories, items=self.items)

    def get(self, request):
        print(self.context)
        return render(request, self.template_name, context=self.context)


def signup_view(request):
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
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

