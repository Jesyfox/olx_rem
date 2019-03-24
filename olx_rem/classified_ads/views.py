from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import Http404
from django.shortcuts import render, get_list_or_404, redirect, HttpResponseRedirect
from django.views.generic import View

from .models import Category, Item


class BaseViewMixin(View):
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


class ShowCategory(BaseViewMixin, View):
    template_name = 'categories.html'

    def get(self, request, hierarchy=None):
        parent = None
        category_slug = hierarchy.split('/')
        root = Category.objects.all()
        for slug in category_slug[:-1]:
            parent = root.get(parent=parent, slug=slug)
        categories = Category.objects.get(parent=parent, slug=category_slug[-1])
        self.context.update(categories=categories)
        try:
            items = Item.objects.filter(
                category__in=Category.objects.get(
                    parent=parent, slug=category_slug[-1]).get_descendants(include_self=True))
            self.context.update(items=items)
            return render(request, self.template_name, self.context)
        except Http404:
            return render(request, self.template_name, self.context)


class Index(BaseViewMixin, View):
    template_name = 'index.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.categories = Category.objects.all()
        self.items = Item.objects.all()
        self.context.update(categories=self.categories, items=self.items)

    def get(self, request):
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

