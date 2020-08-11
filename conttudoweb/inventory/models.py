from django.core.exceptions import ValidationError
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

from conttudoweb.core.models import People
from conttudoweb.core.utils import format_currency


class UnitOfMeasure(models.Model):
    initials = models.CharField('sigla', max_length=5)
    description = models.CharField('descrição', max_length=120)

    def __str__(self):
        return self.initials

    class Meta:
        verbose_name = 'unidade de medida'
        verbose_name_plural = 'unidades de medida'


class Category(MPTTModel):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120, unique=True)
    parent = TreeForeignKey('self', verbose_name='categoria', null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self):
        _description = self.description
        _parent = self.parent
        while _parent:
            _description = "{} / {}".format(_parent.description, _description)
            _parent = _parent.parent
        return _description

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super(Category, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'categoria'
        unique_together = ('description', 'parent')

    class MPTTMeta:
        order_insertion_by = ['description']


class Subcategory(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120)
    category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name, on_delete=models.PROTECT)

    def __str__(self):
        return "%s - %s" % (self.category.description, self.description)

    class Meta:
        verbose_name = 'subcategoria'


class ProductSizeRegister(models.Model):
    description = models.CharField('descrição', max_length=120)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'grade'


class ProductSize(models.Model):
    description = models.CharField('descrição', max_length=6)
    product_size_register = models.ForeignKey('ProductSizeRegister', verbose_name=ProductSizeRegister._meta.verbose_name, on_delete=models.CASCADE)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'item de grade'
        verbose_name_plural = 'itens de grade'
        unique_together = ('description', 'product_size_register')


class Product(models.Model):
    code = models.CharField('código', max_length=20, null=True, blank=True)
    description = models.CharField('descrição', max_length=120, unique=True)
    ncm = models.CharField('NCM', max_length=8, null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name=Category._meta.verbose_name,
                                 on_delete=models.PROTECT, null=True, blank=True)
    subcategory = models.ForeignKey('Subcategory', verbose_name=Subcategory._meta.verbose_name,
                                    on_delete=models.PROTECT, null=True, blank=True)
    unit_of_measure = models.ForeignKey('UnitOfMeasure', verbose_name=UnitOfMeasure._meta.verbose_name,
                                        on_delete=models.PROTECT, null=True, blank=False)
    product_size_register = models.ForeignKey('ProductSizeRegister',
                                              verbose_name=ProductSizeRegister._meta.verbose_name,
                                              on_delete=models.PROTECT, null=True, blank=True)
    cost_price = models.DecimalField('preço de custo', max_digits=15, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField('preço de venda', max_digits=15, decimal_places=2, null=True, blank=True)
    wholesale_selling_price = models.DecimalField('preço de venda atacado', max_digits=15, decimal_places=2, null=True,
                                                  blank=True)

    def __str__(self):
        return "%s (%s)" % (self.description, self.unit_of_measure)

    # TODO: Remover esta função pois agora tem o preço de custo no produto
    def last_cost_price(self):
        return self.cost_price_of_last_purchase()

    last_cost_price.short_description = 'último preço de custo'

    def cost_price_of_last_purchase(self):
        item = self.purchaseitems_set.order_by('-purchase_order__date').first()
        if item:
            # return locale.currency((item.amount / item.quantity), grouping=True)
            return format_currency((item.amount / item.quantity))
        else:
            return format_currency(self.cost_price)
    cost_price_of_last_purchase.short_description = 'preço de custo da última compra'

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


class PackagingType(models.Model):
    description = models.CharField('descrição', max_length=60, unique=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'tipo de embalagem'
        verbose_name_plural = 'tipos de embalagem'
        ordering = ['description']


class Packaging(models.Model):
    product = models.ForeignKey('Product', verbose_name=Product._meta.verbose_name, on_delete=models.CASCADE)
    packaging_type = models.ForeignKey('PackagingType', verbose_name=PackagingType._meta.verbose_name,
                                       on_delete=models.PROTECT)
    quantity = models.DecimalField('quantidade', max_digits=15, decimal_places=2)

    def __str__(self):
        return '{} ({:f})'.format(str(self.packaging_type), self.quantity)

    class Meta:
        verbose_name = 'embalagem'
        verbose_name_plural = 'embalagens'


class Stock(models.Model):
    name = models.CharField('nome', max_length=60, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'almoxarifado'
