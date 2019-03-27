from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

from ..models import Item, Category

from django.contrib.auth.models import User


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='john',
                                        email='jlennon@beatles.com',
                                        password='glass onion')
        category = Category.objects.create(name='Job')
        number_of_items = 13

        for item_id in range(number_of_items):
            Item.objects.create(
                user=user,
                name=f'item {item_id}',
                category=category,
                description='Blah blah',
                price=item_id
            )

    def test_category_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/job/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        response = self.client.get(reverse('classified_ads:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('classified_ads:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_pagination_is_two(self):
        response = self.client.get(reverse('classified_ads:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)

    def test_lists_all_items(self):
        response = self.client.get(reverse('classified_ads:index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?page=6')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?page=7')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 1)
