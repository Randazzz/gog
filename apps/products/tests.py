from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from apps.products.models import Product, ProductCategory
from apps.products.views import ProductsListView


class IndexViewTests(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Grace of the Gods')
        self.assertTemplateUsed(response, 'index.html')


class ProductListViewTests(TestCase):
    fixtures = ['products', 'categories']
    paginate_by = ProductsListView.paginate_by

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertLessEqual(len(response.context_data['object_list']), self.paginate_by)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(Product.available().order_by('id'))[:self.paginate_by]
        )

    def test_list_with_category(self):
        for category in ProductCategory.with_product_count().filter(total_quantity__gte=1):
            path = reverse('products:product_by_category', args=[category.id])
            response = self.client.get(path)
            self._common_tests(response)
            self.assertEqual(
                list(response.context_data['object_list']),
                list(Product.available().filter(category_id=category.id))[:self.paginate_by]
            )

    def test_products_page_diff_no_category(self):
        path_page1 = reverse('products:index') + '?page=1'
        path_page2 = reverse('products:index') + '?page=2'
        response_page1 = self.client.get(path_page1)
        response_page2 = self.client.get(path_page2)
        if response_page2.status_code != 200:
            self.skipTest("Страница 2 не существует, тест пропущен")
        self.assertNotEqual(
            list(response_page1.context_data['object_list']),
            list(response_page2.context_data['object_list'])
        )

    def test_products_page_diff_with_category(self):
        categories = ProductCategory.objects.all()
        skipped_tests = []
        for category in categories:
            path_page1 = reverse('products:product_by_category', args=[category.id]) + '?page=1'
            path_page2 = reverse('products:product_by_category', args=[category.id]) + '?page=2'
            response_page1 = self.client.get(path_page1)
            response_page2 = self.client.get(path_page2)
            if response_page2.status_code != 200:
                skipped_tests.append(category.id)
                continue
            self.assertNotEqual(
                list(response_page1.context_data['object_list']),
                list(response_page2.context_data['object_list'])
            )
        if skipped_tests:
            print(f'Для категорий {skipped_tests} нет 2 страницы')

    def test_all_products_displayed_with_pagination(self):
        pages = (len(Product.available()) + self.paginate_by - 1) // self.paginate_by
        products_in_bd = Product.available().count()
        products_in_site = 0
        for page in range(1, pages + 1):
            path = reverse('products:index') + f'?page={page}'
            response = self.client.get(path)
            products_in_site += response.context_data['object_list'].count()
        self.assertEqual(
            products_in_bd,
            products_in_site,
            "Количество доступных продуктов не совпадает с количеством продуктов на сайте."
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
