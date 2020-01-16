from django.core.exceptions import ValidationError
from django.db import models

from conttudoweb.core.models import People


class Product(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120)
    ncm = models.CharField('NCM', max_length=8, null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'produto'


class ProductBySupplier(models.Model):
    product = models.ForeignKey('inventory.Product', verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE)
    supplier = models.ForeignKey('core.People', verbose_name=People.supplier_label, on_delete=models.CASCADE)
    reference = models.CharField('referência', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120, null=True, blank=True)

    def __str__(self):
        return "%s / Ref: %s / Desc: %s" % (self.supplier, (self.reference or ""), (self.description or ""))

    def clean(self):
        if not self.reference and not self.description:
            raise ValidationError('"Referência" ou "descrição" deve ser preenchido!')

    class Meta:
        verbose_name = 'produto por fornecedor'
        verbose_name_plural = 'produtos por fornecedor'
        unique_together = ['product', 'supplier']
