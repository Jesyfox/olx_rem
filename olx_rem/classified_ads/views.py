from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, \
                             HttpResponseRedirect, render_to_response
from django.views.generic import View
from django.views.generic.edit import DeleteView

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
        categories = Category.objects.all()
        for slug in category_slug[:-1]:
            parent = categories.get(parent=parent, slug=slug)
        categories = Category.objects.get(parent=parent, slug=category_slug[-1])
        self.context.update(categories=categories)
        try:
            items = Item.objects.filter(
                category__in=Category.objects.get(
                    parent=parent, slug=category_slug[-1]).get_descendants(include_self=True))
            paginator = Paginator(items, 2)  # Show 3 contacts per page
            page = request.GET.get('page')
            items = paginator.get_page(page)
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


class ItemUpdate(LoginRequiredMixin, BaseViewMixin, View):
    MAX_NUM_OF_IMAGE = 8
    login_url = '/'
    template_name = 'new_edit_item.html'
    image_formset = modelformset_factory(ItemImage,
                                         form=ItemImageForm,
                                         extra=MAX_NUM_OF_IMAGE)

    def get(self, request, pk=None):
        item = Item.objects.get(pk=pk)
        try:
            photos = get_list_or_404(ItemImage, item=item)
        except Http404:
            photos = None
        item_form = ItemForm(instance=item)
        image_form = self.image_formset(queryset=ItemImage.objects.filter(item_id=pk))
        self.context.update(item_form=item_form, image_form=image_form, images=photos)
        return render(request, self.template_name, self.context)

    def post(self, request, pk=None, **kwargs):
        super().post(request, **kwargs)
        item_form = ItemForm(request.POST, instance=Item.objects.get(pk=pk))
        image_form = self.image_formset(request.POST, request.FILES,
                                        queryset=ItemImage.objects.filter(item_id=pk))
        if item_form.is_valid():
            new_item = item_form.save(commit=False)
            new_item.save()
            if image_form.is_valid():
                item_photos = [img for img in image_form.cleaned_data if img]
                for form in item_photos:
                    if not form['id']:
                        image = form['image']
                        photo = ItemImage(item=new_item, image=image)
                        photo.save()
                    else:
                        form['id'].image = form['image']
                        form['id'].save()
            return redirect('classified_ads:item_info', pk=new_item.id)
        else:
            self.context.update(item_form=item_form, image_form=image_form)
            return render(request, self.template_name, self.context)


class ImageDelete(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        image_model = get_object_or_404(ItemImage, pk=pk)
        item_id = image_model.item.id
        if request.user == image_model.item.user:
            image_model.delete()
            return redirect('classified_ads:item_update', pk=item_id)
        else:
            return redirect('/')


class ItemDelete(LoginRequiredMixin, DeleteView):
    login_url = '/'
    model = Item
    success_url = '/'


class NewItem(LoginRequiredMixin, BaseViewMixin, View):
    login_url = '/'
    template_name = 'new_edit_item.html'
    image_formset = modelformset_factory(ItemImage,
                                         form=ItemImageForm,
                                         extra=8)

    def get(self, request):
        item_form = ItemForm
        image_form = self.image_formset(queryset=ItemImage.objects.none())
        self.context.update(item_form=item_form, image_form=image_form)
        return render(request, self.template_name, self.context)

    def post(self, request, **kwargs):
        super().post(request, **kwargs)
        item_form = ItemForm(request.POST)
        image_form = self.image_formset(request.POST, request.FILES,
                                        queryset=ItemImage.objects.none())
        if item_form.is_valid():
            new_item = item_form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            if image_form.is_valid():
                item_photos = [img for img in image_form.cleaned_data if img]
                for form in item_photos:
                    image = form['image']
                    photo = ItemImage(item=new_item, image=image)
                    photo.save()
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

    def get_query(self, query_string, search_fields):
        query = None
        search_words = query_string.split(' ')
        for word in search_words:
            or_query = None
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: word})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query & or_query
        return query

    def get(self, request):

        if 'search' in request.GET:
            query_string = request.GET.get('search')
            entry_query = self.get_query(query_string, ['name', 'description'])
            items = Item.objects.filter(entry_query)
            self.context.update(items=items, search=query_string)

        paginator = Paginator(self.context.get('items'), 2)  # Show 3 contacts per page
        page = request.GET.get('page')
        items = paginator.get_page(page)
        self.context.update(items=items)
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
