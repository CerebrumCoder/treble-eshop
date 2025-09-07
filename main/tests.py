from django.test import TestCase, Client
from .models import Product

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/burhan_always_exists/')
        self.assertEqual(response.status_code, 404)

    def test_product_creation(self):
        product = Product.objects.create(
          name="SEPATU NIKE",
          price=1000000,
          product_views=1001,
          is_featured=True
        )
        self.assertTrue(product.is_product_hot)
        self.assertTrue(product.is_featured)
        
    def test_product_default_values(self):
        product = Product.objects.create(
          name="JERSEY INDONESIA",
          price=100000,
          product_views=0,
          is_featured=False
        )
        self.assertEqual(product.product_views, 0)
        self.assertFalse(product.is_featured)
        self.assertFalse(product.is_product_hot)

        product.add_stock(10)
        self.assertEqual(product.get_stock(), 10)

    def test_increment_views(self):
        product = Product.objects.create(
          name="Test Product",
          price=100000,
          product_views=0,
          is_featured=False
        )
        initial_views = product.product_views
        product.increment_views()
        self.assertEqual(product.product_views, initial_views + 1)

    def test_is_product_hot_threshold(self):
        # Test product with exactly 20 views (should not be hot)
        product_20 = Product.objects.create(
          name="Product with 20 views",
          price=100000,
          product_views=20,
          is_featured=False
        )
        self.assertFalse(product_20.is_product_hot)

        # Test product with 21 views (should be hot)
        product_21 = Product.objects.create(
          name="Product with 21 views",
          price=100000,
          product_views=21,
          is_featured=False
        )
        self.assertTrue(product_21.is_product_hot)