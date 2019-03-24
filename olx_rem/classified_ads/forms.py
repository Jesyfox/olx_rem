from django.forms import ModelForm
from .models import Item, ItemImage


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'description', 'price', 'negotiable')


class ItemImageForm(ModelForm):
    class Meta:
        model = ItemImage
        fields = ('image',)
