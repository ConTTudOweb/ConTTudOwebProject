from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from .test_model import ModelAdminTest
from ..admin import FederativeUnitModelAdmin
from ..models import FederativeUnit

_initials = 'FU'
_name = 'Federative Unit 1'


def create_federative_unit(**kwargs):
    kwargs.setdefault('initials', _initials)
    kwargs.setdefault('name', _name)
    federative_unit = FederativeUnit.objects.create(**kwargs)
    return federative_unit


class FederativeUnitModelTest(FastTenantTestCase):
    def setUp(self):
        self.federative_unit = create_federative_unit()

    def test_create(self):
        self.assertTrue(FederativeUnit.objects.exists())

    def test_str(self):
        self.assertEqual(_name, str(self.federative_unit))

    def test_unique_initials(self):
        with self.assertRaises(IntegrityError):
            create_federative_unit(name='Other name')


class FederativeUnitAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = FederativeUnitModelAdmin
    Model = FederativeUnit
