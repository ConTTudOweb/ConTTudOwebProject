from django.db import models

from conttudoweb.core import utils
from conttudoweb.core.models import People
from conttudoweb.inventory.models import Product


class Vendor(models.Model):
    name = models.CharField('nome', max_length=60)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'vendedor'
        verbose_name_plural = 'vendedores'


class SaleOrder(models.Model):
    customer = models.ForeignKey('core.People', verbose_name=People.customer_label, on_delete=models.PROTECT,
                                 limit_choices_to={'customer': True}, null=True, blank=True)
    code = models.CharField('código', max_length=20, null=True, blank=True)
    date = models.DateField('data', null=True, blank=False)
    items = models.ManyToManyField('inventory.Product', through='SaleOrderItems')

    def amount_admin(self):
        net_total = 0
        for i in self.saleorderitems_set.all():
            net_total += i._net_total()
        return utils.format_currency(net_total)
    amount_admin.short_description = 'valor líquido'
    amount = property(amount_admin)

    def __str__(self):
        return "#%s - %s" % (self.id, self.date)

    class Meta:
        verbose_name = utils.sale_order_verbose_name
        verbose_name_plural = 'pedidos de venda'


class SaleOrderItems(models.Model):
    sale_order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', verbose_name=Product._meta.verbose_name, on_delete=models.PROTECT)
    quantity = models.DecimalField('quantidade', max_digits=15, decimal_places=2)
    price = models.DecimalField('preço', max_digits=15, decimal_places=2)
    discount_percentage = models.DecimalField('% desconto', max_digits=5, decimal_places=2, null=True, blank=True)

    def _net_total(self):
        if self.quantity and self.price:
            gross_total = self.quantity * self.price  # total bruto
            total_discount = 0
            if self.discount_percentage:
                total_discount = gross_total * (self.discount_percentage / 100)  # total desconto
            net_total = gross_total - total_discount  # total líquido
            return net_total

    def amount_admin(self):
        if self._net_total():
            return utils.format_currency(self._net_total())
        return ""
    amount_admin.short_description = 'valor líquido'
    amount = property(amount_admin)

    class Meta:
        verbose_name = 'item de venda'
        verbose_name_plural = 'itens de venda'
