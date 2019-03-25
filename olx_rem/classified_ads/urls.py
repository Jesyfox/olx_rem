from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

from . import views
from . import api_views

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^rest/swagger/$', schema_view),

    url(r'^rest/items/$', api_views.ItemViewSet.as_view({'get': 'list'})),
    url(r'^rest/items/create/$', api_views.ItemViewSet.as_view({'post': 'create'})),
    url(r'^rest/items/retrieve/(?P<pk>[0-9]+)/$', api_views.ItemViewSet.as_view({'get': 'retrieve'})),
    url(r'^rest/items/update/(?P<pk>[0-9]+)/$', api_views.ItemViewSet.as_view({'put': 'update'})),
    url(r'^rest/items/delete/(?P<pk>[0-9]+)/$', api_views.ItemViewSet.as_view({'delete': 'destroy'})),

    url(r'^rest/category/$', api_views.CategoryViewSet.as_view({'get': 'list'})),
    url(r'^rest/category/create/$', api_views.CategoryViewSet.as_view({'post': 'create'})),
    url(r'^rest/category/retrieve/(?P<pk>[0-9]+)/$', api_views.CategoryViewSet.as_view({'get': 'retrieve'})),
    url(r'^rest/category/update/(?P<pk>[0-9]+)/$', api_views.CategoryViewSet.as_view({'put': 'update'})),
    url(r'^rest/category/delete/(?P<pk>[0-9]+)/$', api_views.CategoryViewSet.as_view({'delete': 'destroy'})),

    url(r'^rest/users/$', api_views.UserViewSet.as_view({'get': 'list'})),


]

urlpatterns += [
    path('', views.Index.as_view(), name='index'),
    path('sign_up/', views.signup_view, name='sign_up'),
    path('logout/', LogoutView.as_view(template_name='index.html', next_page='/'), name='logout'),
    path('category/<path:hierarchy>/', views.ShowCategory.as_view(), name='category'),
    path('items/<int:pk>', views.ItemInfo.as_view(), name='item_info'),
    path('new_item/', views.NewItem.as_view(), name='new_item'),
    path('update/<int:pk>', views.ItemUpdate.as_view(), name='item_update'),
    path('delete/<int:pk>', views.ItemDelete.as_view(), name='item_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
