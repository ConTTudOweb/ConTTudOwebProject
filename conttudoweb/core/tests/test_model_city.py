from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from .test_model import ModelAdminTest
from .test_model_federative_unit import create_federative_unit
from ..admin import CityModelAdmin
from ..models import City

_name = 'City 1'


def create_city(**kwargs):
    city = City.objects.create(
        name=_name,
        **kwargs
    )
    return city


class CityModelTest(FastTenantTestCase):
    def setUp(self):
        self.uf = create_federative_unit()
        self.city = create_city(uf=self.uf)

    def test_create(self):
        self.assertTrue(City.objects.exists())

    def test_str(self):
        self.assertEqual("{}-{}".format(_name, self.uf.initials), str(self.city))

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            create_city(uf=self.uf)


class CityAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = CityModelAdmin
    Model = City
