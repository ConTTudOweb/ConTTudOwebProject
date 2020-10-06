from django.db import models
from django.utils import timezone

from conttudoweb.core import utils
from conttudoweb.core.models import People
from conttudoweb.inventory.models import Product, Packaging


# class Vendor(models.Model):
#     name = models.CharField('nome', max_length=60)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'vendedor'
#         verbose_name_plural = 'vendedores'


class SaleOrder(models.Model):
    customer = models.ForeignKey('core.People', verbose_name=People.customer_label, on_delete=models.PROTECT,
                                 limit_choices_to={'customer': True}, null=True, blank=True)
    date_order = models.DateField('data de emissão', default=timezone.now)
    validity_date = models.DateField('data de validade', null=True, blank=True)
    discount_percentage = models.DecimalField('% desconto', max_digits=5, decimal_places=2, null=True, blank=True)

    @property
    def gross_total(self):
        gross_total = 0
        for i in self.saleorderitems_set.all():
            gross_total += i.gross_total or 0

        return gross_total

    @property
    def net_total(self):
        net_total = 0
        for i in self.saleorderitems_set.all():
            net_total += i.net_total or 0

        return net_total

    def net_total_admin(self):
        net_total = 0
        for i in self.saleorderitems_set.all():
            net_total += i.net_total
        return utils.format_currency(net_total)
    net_total_admin.short_description = 'valor líquido'

    def __str__(self):
        return '#{:06}'.format(self.id)

    class Meta:
        verbose_name = utils.sale_order_verbose_name
        verbose_name_plural = utils.sale_order_verbose_name_plural


class SaleOrderItems(models.Model):
    sale_order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', verbose_name=Product._meta.verbose_name, on_delete=models.PROTECT)
    quantity = models.DecimalField('quantidade', max_digits=15, decimal_places=2)
    price = models.DecimalField('preço', max_digits=15, decimal_places=2)
    discount_percentage = models.DecimalField('% desconto', max_digits=5, decimal_places=2, null=True, blank=True)
    packing = models.ForeignKey('inventory.Packaging', verbose_name=Packaging._meta.verbose_name,
                                on_delete=models.PROTECT, null=True, blank=True)
    gross_total = models.DecimalField('valor bruto', max_digits=15, decimal_places=2, null=True, blank=True,
                                      editable=False)
    net_total = models.DecimalField('valor líquido', max_digits=15, decimal_places=2, null=True, blank=True,
                                    editable=False)

    class Meta:
        verbose_name = 'item de venda'
        verbose_name_plural = 'itens de venda'

    # @property
    # def _net_total(self):
    #     if self.quantity and self.price:
    #         gross_total = self.quantity * self.price  # total bruto
    #         total_discount = 0
    #         _discount_percentage = self.discount_percentage or self.sale_order.discount_percentage
    #         if _discount_percentage:
    #             total_discount = gross_total * (_discount_percentage / 100)  # total desconto
    #         net_total = gross_total - total_discount  # total líquido
    #         return net_total

    def amount_admin(self):
        # if self._net_total:
        if self.net_total:
            # return utils.format_currency(self._net_total)
            return utils.format_currency(self.net_total)
        return ""
    amount_admin.short_description = 'valor líquido'
    amount = property(amount_admin)

    def save(self, *args, **kwargs):
        if self.quantity and self.price:
            gross_total = self.quantity * self.price  # total bruto
            total_discount = 0
            _discount_percentage = self.discount_percentage or self.sale_order.discount_percentage
            if _discount_percentage:
                total_discount = gross_total * (_discount_percentage / 100)  # total desconto
            net_total = gross_total - total_discount  # total líquido

            self.gross_total = gross_total
            self.net_total = net_total

        super().save(*args, **kwargs)
