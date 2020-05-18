# Generated by Django 3.0.5 on 2020-05-16 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20200516_1419'),
        ('purchase', '0004_auto_20200203_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Product', verbose_name='produto'),
        ),
    ]