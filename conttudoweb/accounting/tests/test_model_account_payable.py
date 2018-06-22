from django.test import TestCase

from ...core.tests.test_model import ModelAdminTest
from ..models import AccountPayable
from ..admin import AccountPayableModelAdmin
from .test_model_account import create_account, AccountAdminTest


class AccountPayableModelTest(TestCase):
    def setUp(self):
        self._description = 'Account Payable 1'
        self.accountPayable = AccountPayable.objects.create(
            **create_account(self._description)
        )

    def test_create(self):
        self.assertTrue(AccountPayable.objects.exists())

    def test_str(self):
        self.assertEqual(self._description, str(self.accountPayable))

    # TODO: Bolar uma forma de testar se o campo person para este modelo trás apenas fornecedores!


class AccountPayableAdminTest(AccountAdminTest, ModelAdminTest, TestCase):
    ModelAdmin = AccountPayableModelAdmin
    Model = AccountPayable
