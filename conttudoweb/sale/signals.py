from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import SaleOrderItems


@receiver(pre_save, sender=SaleOrderItems)
def save_sale_order_item(sender, instance: SaleOrderItems, **kwargs):
    print('passouuuuuuuuuuuuuuuuuuuuu')
    if instance.quantity and instance.price:
        gross_total = instance.quantity * instance.price  # total bruto
        total_discount = 0
        _discount_percentage = instance.discount_percentage or instance.sale_order.discount_percentage
        if _discount_percentage:
            total_discount = gross_total * (_discount_percentage / 100)  # total desconto
        net_total = gross_total - total_discount  # total líquido

        instance.net_total = net_total
