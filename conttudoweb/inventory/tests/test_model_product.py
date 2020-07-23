from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..models import Product
from ..admin import ProductModelAdmin
from ...core.tests.test_model import ModelAdminTest


_description = 'Product 1'


def get_fields_product():
    return {
        'description': _description
    }


def create_product():
    product = Product.objects.create(**get_fields_product())
    return product


class ProductModelTest(FastTenantTestCase):
    def setUp(self):
        self.product = create_product()

    def test_create(self):
        self.assertTrue(Product.objects.exists())

    def test_str(self):
        self.assertEqual("%s (%s)" % (_description, None), str(self.product))

    def test_unique_description(self):
        with self.assertRaises(IntegrityError):
            create_product()


class ProductAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = ProductModelAdmin
    Model = Product
