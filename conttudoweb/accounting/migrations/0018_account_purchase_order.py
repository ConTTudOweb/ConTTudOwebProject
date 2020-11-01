# Generated by Django 3.1.2 on 2020-10-12 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0005_auto_20200516_1802'),
        ('accounting', '0017_auto_20201010_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='purchase_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='purchase.purchaseorder', verbose_name='ordem de compra'),
        ),
    ]