from django.test import TestCase
from tenant_schemas.test.cases import FastTenantTestCase

from ..models import DepositAccount
from ..admin import DepositAccountModelAdmin
from ...core.tests.test_model import ModelAdminTest
# from ...core.tests.test_model_entity import get_or_create_entity


class DepositAccountModelTest(FastTenantTestCase):
    def setUp(self):
        self._name = 'Deposit Account 1'
        self.depositAccount = DepositAccount.objects.create(
            # entity=get_or_create_entity(),
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
    exclude = ('entity',)
