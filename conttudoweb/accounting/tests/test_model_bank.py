from django.db import IntegrityError
from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..admin import BankModelAdmin
from ..models import Bank
from ...core.tests.test_model import ModelAdminTest

_code = 'XXX'
_description = 'Bank 1'


def get_fields_bank():
    return {
        'code': _code,
        'description': _description
    }


def create_bank():
    bank = Bank.objects.create(**get_fields_bank())
    return bank


class BankModelTest(FastTenantTestCase):
    def setUp(self):
        self.bank = create_bank()

    def test_create(self):
        self.assertTrue(Bank.objects.exists())

    def test_str(self):
        self.assertEqual("{0} - {1}".format(_code, _description), str(self.bank))

    def test_unique_code(self):
        with self.assertRaises(IntegrityError):
            create_bank()


class BankAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = BankModelAdmin
    Model = Bank
