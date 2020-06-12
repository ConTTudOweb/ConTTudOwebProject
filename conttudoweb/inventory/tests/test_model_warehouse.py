from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..models import Warehouse
from ..admin import WarehouseModelAdmin
from ...core.tests.test_model import ModelAdminTest


_name = 'Warehouse 1'


def get_fields_warehouse():
    return {
        'name': _name
    }


def create_warehouse():
    warehouse = Warehouse.objects.create(**get_fields_warehouse())
    return warehouse


class WarehouseModelTest(FastTenantTestCase):
    def setUp(self):
        self.warehouse = create_warehouse()

    def test_create(self):
        self.assertTrue(Warehouse.objects.exists())

    def test_str(self):
        self.assertEqual(_name, str(self.warehouse))

    def test_unique_code(self):
        with self.assertRaises(IntegrityError):
            create_warehouse()


class WarehouseAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = WarehouseModelAdmin
    Model = Warehouse
