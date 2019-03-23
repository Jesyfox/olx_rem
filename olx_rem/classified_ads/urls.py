from django.conf.urls import url
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [
    url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
    path('api/login', views.login, name='login')
]
