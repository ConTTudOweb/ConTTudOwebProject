from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..admin import ClassificationCenterModelAdmin
from ..models import ClassificationCenter
from ...core.tests.test_model import ModelAdminTest

_name = 'Classification Center 1'
_name_cost = 'Cost Center 1'
_name_revenue = 'Revenue Center 1'


def create_classification_center(**kwargs):
    classification_center = ClassificationCenter.objects.create(
        **kwargs
    )
    return classification_center


class ClassificationCenterModelTest(FastTenantTestCase):
    def setUp(self):
        self.classification_center = create_classification_center(name=_name)

    def test_create(self):
        self.assertTrue(ClassificationCenter.objects.exists())

    def test_create_cost_center(self):
        classification_center_cost = create_classification_center(cost_center=True)
        self.assertTrue(classification_center_cost.is_cost_center())

    def test_create_revenue_center(self):
        classification_center_revenue = create_classification_center(revenue_center=True)
        self.assertTrue(classification_center_revenue.is_revenue_center())

    def test_str(self):
        self.assertEqual(_name, str(self.classification_center))

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            create_classification_center(name=_name)


class ClassificationCenterAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = ClassificationCenterModelAdmin
    Model = ClassificationCenter
    # exclude = ('entity',)
