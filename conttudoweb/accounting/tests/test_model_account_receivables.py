from django.test import TestCase
from tenant_schemas.test.cases import FastTenantTestCase

from ...core.tests.test_model import ModelAdminTest
from ..models import AccountReceivable
from ..admin import AccountReceivableModelAdmin
from .test_model_account import create_account, AccountAdminTest


class AccountReceivablesModelTest(FastTenantTestCase):
    def setUp(self):
        self._description = 'Account Receivables 1'
        self.accountReceivables = AccountReceivable.objects.create(
            **create_account(self._description)
        )

    def test_create(self):
        self.assertTrue(AccountReceivable.objects.exists())

    def test_str(self):
        self.assertEqual(self._description, str(self.accountReceivables))

    # TODO: Bolar uma forma de testar se o campo person para este modelo trás apenas fornecedores!


class AccountReceivablesAdminTest(AccountAdminTest, ModelAdminTest, TestCase):
    ModelAdmin = AccountReceivableModelAdmin
    Model = AccountReceivable
