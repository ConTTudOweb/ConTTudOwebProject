from django.test import TestCase
from django_tenants.test.cases import FastTenantTestCase

from ..admin import DepositAccountModelAdmin
from ..models import DepositAccount
from ...core.tests.test_model import ModelAdminTest


class DepositAccountModelTest(FastTenantTestCase):
    def setUp(self):
        self._name = 'Deposit Account 1'
        self.depositAccount = DepositAccount.objects.create(
            type=DepositAccount.DepositAccountTypes.current_account.value,
            bank=None,
            agency_number=None,
            agency_digit=None,
            account_number=None,
            account_digit=None,
            name=self._name
        )

    def test_create(self):
        self.assertTrue(DepositAccount.objects.exists())

    def test_str(self):
        self.assertEqual(self._name, str(self.depositAccount))


class DepositAccountAdminTest(ModelAdminTest, TestCase):
    ModelAdmin = DepositAccountModelAdmin
    Model = DepositAccount
