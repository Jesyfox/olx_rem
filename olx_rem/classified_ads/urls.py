from django.conf.urls import url
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sign_up', views.signup_view, name='sign_up'),
    path('logout', LogoutView.as_view(template_name='index.html', next_page='/'), name='logout'),
    path('category/<path:hierarchy>/', views.ShowCategory.as_view(), name='category'),
    path('items/<int:pk>', views.ItemInfo.as_view(), name='item_info')
]
