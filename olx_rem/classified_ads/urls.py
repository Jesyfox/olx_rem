from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('sign_up/', views.signup_view, name='sign_up'),
    path('logout/', LogoutView.as_view(template_name='index.html', next_page='/'), name='logout'),
    path('category/<path:hierarchy>/', views.ShowCategory.as_view(), name='category'),
    path('items/<int:pk>', views.ItemInfo.as_view(), name='item_info'),
    path('new_item/', views.NewItem.as_view(), name='new_item')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
