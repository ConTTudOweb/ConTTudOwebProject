# Generated by Django 3.0.8 on 2020-08-08 14:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0006_auto_20200808_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleorder',
            name='date_order',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de emissão'),
        ),
    ]
