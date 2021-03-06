# Generated by Django 3.0.7 on 2020-07-18 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsize',
            name='product_size_register',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ProductSizeRegister', verbose_name='grade'),
        ),
        migrations.AlterUniqueTogether(
            name='productsize',
            unique_together={('description', 'product_size_register')},
        ),
    ]
