from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import viewsets

from .models import Category, Item, ItemImage
from . import serializers


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        model_object = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(model_object)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(ItemViewSet, self).create(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        model_object = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(model_object)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).create(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
