# Generated by Django 3.0.8 on 2020-08-08 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0007_auto_20200808_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleorder',
            name='date_order',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='data de emissão'),
        ),
    ]
