# Generated by Django 3.0.8 on 2020-07-25 16:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0003_vendor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Vendor',
        ),
        migrations.AlterModelOptions(
            name='saleorder',
            options={'verbose_name': 'ordem de venda', 'verbose_name_plural': 'ordens de venda'},
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='code',
        ),
        migrations.RemoveField(
            model_name='saleorder',
            name='date',
        ),
        migrations.AddField(
            model_name='saleorder',
            name='date_order',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 25, 16, 1, 4, 656447, tzinfo=utc), verbose_name='data de emissão'),
        ),
        migrations.AddField(
            model_name='saleorder',
            name='validity_date',
            field=models.DateField(blank=True, null=True, verbose_name='data de validade'),
        ),
    ]
