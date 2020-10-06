# Generated by Django 3.0.9 on 2020-08-19 19:33

from django.db import migrations
from django_tenants.utils import get_public_schema_name


def recalcula_itens(apps, schema_editor):
    if schema_editor.connection.schema_name != get_public_schema_name():
        sale_ordem_item_model = apps.get_model("sale", "SaleOrderItems")
        itens = sale_ordem_item_model.objects.all()
        for item in itens:
            if item.quantity and item.price:
                gross_total = item.quantity * item.price  # total bruto
                total_discount = 0
                _discount_percentage = item.discount_percentage or item.sale_order.discount_percentage
                if _discount_percentage:
                    total_discount = gross_total * (_discount_percentage / 100)  # total desconto
                item.net_total = gross_total - total_discount  # total líquido
                item.save()


def do_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0011_saleorderitems_net_total'),
    ]

    operations = [
        migrations.RunPython(recalcula_itens, reverse_code=do_nothing),
    ]