from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Item, ItemImage


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'category', 'description', 'price', 'negotiable')

    def clean_negotiable(self):
        price = self.cleaned_data.get('price', 0)
        if price is None:
            price = 0
        negotiable = self.cleaned_data.get('negotiable')
        if not price and not negotiable:
            raise ValidationError(
                'price must be grater than 0 or "negotiable" must be present!!!',
                code='invalid',
            )
        if price < 0:
            raise ValidationError(
                'price must be grater than 0',
                code='invalid',
            )
        return negotiable



class ItemImageForm(ModelForm):
    class Meta:
        model = ItemImage
        fields = ('image',)
