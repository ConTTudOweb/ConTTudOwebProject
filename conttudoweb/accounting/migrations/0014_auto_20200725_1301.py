# Generated by Django 3.0.8 on 2020-07-25 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0004_auto_20200725_1301'),
        ('accounting', '0013_auto_20200623_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='sale_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale.SaleOrder', verbose_name='ordem de venda'),
        ),
    ]
