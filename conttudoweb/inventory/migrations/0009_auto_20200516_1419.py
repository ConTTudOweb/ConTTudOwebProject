# Generated by Django 3.0.5 on 2020-05-16 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_auto_20200203_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSizeRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=120, verbose_name='descrição')),
            ],
            options={
                'verbose_name': 'grade',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='cost_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='preço de custo'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='preço de venda'),
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_selling_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='preço de venda atacado'),
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=6, verbose_name='descrição')),
                ('product_size_register', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.ProductSizeRegister', verbose_name='grade')),
            ],
            options={
                'verbose_name': 'item de grade',
                'verbose_name_plural': 'itens de grade',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='product_size_register',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.ProductSizeRegister', verbose_name='grade'),
        ),
    ]
