from django.db import models

from conttudoweb.core import utils
from conttudoweb.core.models import People
from conttudoweb.inventory.models import Product


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey('core.People', verbose_name=People.supplier_label, on_delete=models.PROTECT,
                                 limit_choices_to={'supplier': True})
    code = models.CharField('código', max_length=20, null=True, blank=True)
    date = models.DateField('data', null=True, blank=False)
    items = models.ManyToManyField('inventory.Product', through='PurchaseItems')

    @property
    def amount_total(self):
        amount_total = 0
        for i in self.purchaseitems_set.all():
            amount_total += (i.amount * i.quantity) or 0

        return amount_total

    def __str__(self):
        return "#%s - %s" % (self.id, self.supplier)

    class Meta:
        verbose_name = utils.purchase_order_verbose_name
        verbose_name_plural = utils.purchase_order_verbose_name_plural


class PurchaseItems(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', verbose_name=Product._meta.verbose_name, on_delete=models.PROTECT)
    quantity = models.DecimalField('quantidade', max_digits=15, decimal_places=2)
    # price = models.DecimalField('preço', max_digits=15, decimal_places=2)
    amount = models.DecimalField('valor total', max_digits=15, decimal_places=2)

    class Meta:
        verbose_name = 'item de compra'
        verbose_name_plural = 'itens de compra'

    def __str__(self):
        return f'ID {self.id}'
