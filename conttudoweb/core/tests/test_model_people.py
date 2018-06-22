from django.db import IntegrityError
from django.test import TestCase

from ..models import People
from ..admin import PeopleModelAdmin
from .test_model import ModelAdminTest


_name = 'People 1'
_name_customer = 'Customer 1'
_name_supplier = 'Supplier 1'


def create_people(**kwargs):
    people = People.objects.create(
        **kwargs
    )
    return people


class PeopleModelTest(TestCase):
    def setUp(self):
        self.people = create_people(name=_name)

    def test_create(self):
        self.assertTrue(People.objects.exists())

    def test_create_customer(self):
        person_customer = create_people(name=_name_customer, customer=True)
        self.assertTrue(person_customer.is_customer())

    def test_create_supplier(self):
        person_supplier = create_people(name=_name_supplier, supplier=True)
        self.assertTrue(person_supplier.is_supplier())

    def test_str(self):
        self.assertEqual(_name, str(self.people))

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            create_people(name=_name)


class PeopleAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = PeopleModelAdmin
    Model = People
