from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Item, Category


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        category = Category.objects.create(name='Job')
        Item.objects.create(user=user,
                            name='Drummer',
                            category=category,
                            description='Looking for drummer',
                            price=10)

    def test_description_max_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('description').max_length
        self.assertEquals(max_length, 5000)

    def test_price_label(self):
        item = Item.objects.get(id=1)
        self.assertGreater(item.price, 0)

    def test_negotiable_label(self):
        item = Item.objects.get(id=1)
        self.assertFalse(item.negotiable)
