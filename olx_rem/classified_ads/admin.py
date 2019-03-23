from django.contrib import admin
from django.contrib.sites.models import Site
from mptt.admin import DraggableMPTTAdmin

from .models import Category, Item


admin.site.register(Item)
admin.site.register(Category, DraggableMPTTAdmin)

admin.site.unregister(Site)
