from django.test import TestCase
from tenant_schemas.test.cases import FastTenantTestCase

from conttudoweb.accounting.utils import AccountFrequencys
from ...core.tests.test_model import ModelAdminTest
from ..models import Account, AccountPayable
from ..admin import AccountPayableModelAdmin
from .test_model_account import create_account, AccountAdminTest


class AccountPayableModelTest(FastTenantTestCase):
    def setUp(self):
        self._description = 'Account Payable 1'
        self._descriptionParcelled = 'Account Payable 1 parcelled'

        self.accountPayable = AccountPayable.objects.create(
            **create_account(self._description)
        )
        self.accountPayableParcelled = AccountPayable.objects.create(
            **create_account(
                self._descriptionParcelled,
                **{'type': Account.AccountTypes.parcelled.value,
                   'frequency': AccountFrequencys.weekly.value,
                   'number_of_parcels': 3}
            )
        )

    def test_create(self):
        self.assertTrue(AccountPayable.objects.exists())

    def test_create_parcelled(self):
        self.assertEqual(3, AccountPayable.objects.filter(parent=self.accountPayableParcelled.pk).count())
        _last = AccountPayable.objects.filter(parent=self.accountPayableParcelled.pk).\
            exclude(pk=self.accountPayableParcelled.pk).last()
        self.assertNotEqual(self.accountPayableParcelled.due_date, _last.due_date)

    def test_str(self):
        self.assertEqual(self._description, str(self.accountPayable))

        _descriptionParcelled = str(str(self._descriptionParcelled) + ' - 1/3')
        self.assertEqual(_descriptionParcelled, str(self.accountPayableParcelled))

    # TODO: Bolar uma forma de testar se o campo person para este modelo trás apenas fornecedores!


class AccountPayableAdminTest(AccountAdminTest, ModelAdminTest, TestCase):
    ModelAdmin = AccountPayableModelAdmin
    Model = AccountPayable
