from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

from ..models import Item, Category

from django.contrib.auth.models import User


class ItemListViewTest(TestCase):
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

    def test_search_items(self):
        response = self.client.get(reverse('classified_ads:index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('classified_ads:index') + '?search=item 10')
        self.assertEqual(len(response.context['items']), 1)

    def test_price_search_items(self):
        response = self.client.get(reverse('classified_ads:index') + '?min_price=2&max_price=6')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?min_price=2&max_price=6&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 2)
        response = self.client.get(reverse('classified_ads:index') + '?min_price=2&max_price=6&page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['items']) == 1)

    def test_item_info(self):
        response = self.client.get('/items/10/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item_info.html')

    def test_delete_item(self):
        response = self.client.post('/delete/10/')
        self.assertRedirects(response, '/?next=/delete/10/')
        login = self.client.login(username='john', password='glass onion')
        response = self.client.get('/delete/10/')
        self.assertTemplateUsed(response, 'classified_ads/item_confirm_delete.html')
        self.assertContains(response, 'Are you sure you want to delete')
        response = self.client.post('/delete/10/', args=(10,), follow=True)
        self.assertRedirects(response, '/')
