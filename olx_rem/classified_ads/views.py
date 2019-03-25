from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Category, Item, ItemImage
from .forms import ItemForm, ItemImageForm


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


class ItemInfo(BaseViewMixin, View):
    template_name = 'item_info.html'

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        try:
            photos = get_list_or_404(ItemImage, item=item)
        except Http404:
            photos = None
        self.context.update(items=item, photos=photos)
        return render(request, self.template_name, self.context)


class ItemUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/'
    model = Item
    fields = ('name', 'category', 'description', 'price', 'negotiable')
    template_name_suffix = '_update_form'
    success_url = '/'


class ItemDelete(LoginRequiredMixin, DeleteView):
    login_url = '/'
    model = Item
    success_url = '/'


class NewItem(LoginRequiredMixin, BaseViewMixin, View):
    login_url = '/'
    template_name = 'new_item.html'

    def get(self, request):
        item_form = ItemForm
        image_form = ItemImageForm
        self.context.update(item_form=item_form, image_form=image_form)
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        super().post(request, **kwargs)
        item_form = ItemForm(request.POST)
        image_form = ItemImageForm(request.POST, request.FILES)
        if item_form.is_valid():
            new_item = item_form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            if image_form.is_valid() and image_form.cleaned_data.get('image'):
                print('validated!')
                new_image = image_form.save(commit=False)
                new_image.item = new_item
                new_image.save()
        else:
            self.context.update(item_form=item_form, image_form=image_form)
            return render(request, self.template_name, self.context)
        return redirect('/')


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

