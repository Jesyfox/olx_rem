from rest_framework import serializers

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Item, Category, ItemImage


class RecursiveField(serializers.BaseSerializer):
    def to_representation(self, value):
        ParentSerializer = self.parent.parent.__class__
        serializer = ParentSerializer(value, context=self.context)
        return serializer.data

    def to_internal_value(self, data):
        ParentSerializer = self.parent.parent.__class__
        Model = ParentSerializer.Meta.model
        try:
            instance = Model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Object {0} not found'.format(
                    Model().__class__.__name__
                )
            )
        return instance


class CategorySerializer(serializers.ModelSerializer):
    subcategories = RecursiveField(source='children',
                                   many=True, required=False, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories')


class ItemUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ItemImageAtachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemImage
        fields = ('id', 'image')


class ItemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    user = ItemUserSerializer()
    images = ItemImageAtachmentSerializer(many=True)
    category = ItemCategorySerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'description', 'price', 'negotiable', 'images', 'user')


class ItemImageSerializer(serializers.ModelSerializer):
    item = ItemSerializer(many=True)

    class Meta:
        model = ItemImage
        fields = ('id', 'image', 'item')


class UserItemSerializer(serializers.ModelSerializer):
    images = ItemImageAtachmentSerializer(many=True)
    category = ItemCategorySerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'images')


class UserSerializer(serializers.ModelSerializer):
    items = UserItemSerializer(many=True, read_only=True, source='user')

    class Meta:
        model = User
        fields = ('id', 'username', 'items')
