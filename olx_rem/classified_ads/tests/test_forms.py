from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import ItemForm
from ..models import Category


class ItemFromTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        category = Category.objects.create(name='Job')

    def test_valid_form(self):
        item = {'name': 'Drummer',
                'category': 1,
                'description': 'looking for drummer',
                'price': 10,
                'negotiable': False,
                'user': 1}
        form = ItemForm(item)
        self.assertTrue(form.is_valid())

    def test_price_none_negotiable_false(self):
        item = {'name': 'Drummer',
                'category': 1,
                'description': 'looking for drummer',
                'price': 0,
                'negotiable': False,
                'user': 1}
        form = ItemForm(item)
        self.assertFalse(form.is_valid())

    def test_price(self):
        item = {'name': 'Drummer',
                'category': 1,
                'description': 'looking for drummer',
                'price': -10,
                'negotiable': True,
                'user': 1}
        form = ItemForm(item)
        self.assertFalse(form.is_valid())

    def test_negotiable(self):
        item = {'name': 'Drummer',
                'category': 1,
                'description': 'looking for drummer',
                'price': None,
                'negotiable': True,
                'user': 1}
        form = ItemForm(item)
        self.assertTrue(form.is_valid())
