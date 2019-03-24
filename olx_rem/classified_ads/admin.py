from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Item, ItemImage


admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(Category, DraggableMPTTAdmin)
