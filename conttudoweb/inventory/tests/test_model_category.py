from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..models import Category
from ..admin import CategoryModelAdmin
from ...core.tests.test_model import ModelAdminTest


_description = 'Category 1'


def get_fields_category():
    return {
        'description': _description
    }


def create_category():
    category = Category.objects.create(**get_fields_category())
    return category


class CategoryModelTest(FastTenantTestCase):
    def setUp(self):
        self.category = create_category()

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_str(self):
        self.assertEqual(_description, str(self.category))

    def test_unique_description(self):
        with self.assertRaises(IntegrityError):
            create_category()


class CategoryAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = CategoryModelAdmin
    Model = Category
