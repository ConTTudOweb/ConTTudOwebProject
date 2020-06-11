from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..admin import CategoryModelAdmin
from ...accounting.models import Category
from ...core.tests.test_model import ModelAdminTest


class CategoryModelTest(FastTenantTestCase):
    def setUp(self):
        self._description = 'Category 1'
        self.category = Category.objects.create(
            description=self._description
        )

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_str(self):
        self.assertEqual(self._description, str(self.category))


class CategoryAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = CategoryModelAdmin
    Model = Category
