from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Item


admin.site.register(Item)
admin.site.register(Category, DraggableMPTTAdmin)

