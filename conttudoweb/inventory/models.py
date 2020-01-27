from django.core.exceptions import ValidationError
from django.db import models

from conttudoweb.core.models import People


class Category(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'categoria'


class Subcategory(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120)
    category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name, on_delete=models.PROTECT)

    def __str__(self):
        return "%s - %s" % (self.category.description, self.description)

    class Meta:
        verbose_name = 'subcategoria'


class Product(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120)
    ncm = models.CharField('NCM', max_length=8, null=True, blank=True)
    subcategory = models.ForeignKey('Subcategory', verbose_name=Subcategory._meta.verbose_name, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'produto'


class ProductBySupplier(models.Model):
    product = models.ForeignKey('inventory.Product', verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE)
    supplier = models.ForeignKey('core.People', verbose_name=People.supplier_label, on_delete=models.CASCADE,
                                 limit_choices_to={'supplier': True})
    reference = models.CharField('referência', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120, null=True, blank=True)

    def __str__(self):
        return "%s / Ref: %s / Desc: %s" % (self.supplier, (self.reference or ""), (self.description or ""))

    def clean(self):
        if not self.reference and not self.description:
            raise ValidationError('"Referência" ou "descrição" deve ser preenchido!')

    class Meta:
        verbose_name = 'referência por fornecedor'
        verbose_name_plural = 'referências por fornecedor'
        unique_together = ['product', 'supplier']
