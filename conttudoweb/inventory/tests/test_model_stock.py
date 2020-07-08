from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..models import Stock
from ..admin import StockModelAdmin
from ...core.tests.test_model import ModelAdminTest


_name = 'Stock 1'


def get_fields_stock():
    return {
        'name': _name
    }


def create_stock():
    stock = Stock.objects.create(**get_fields_stock())
    return stock


class StockModelTest(FastTenantTestCase):
    def setUp(self):
        self.stock = create_stock()

    def test_create(self):
        self.assertTrue(Stock.objects.exists())

    def test_str(self):
        self.assertEqual(_name, str(self.stock))

    def test_unique_code(self):
        with self.assertRaises(IntegrityError):
            create_stock()


class StockAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = StockModelAdmin
    Model = Stock
