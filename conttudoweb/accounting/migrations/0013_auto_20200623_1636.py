# Generated by Django 3.0.7 on 2020-06-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0012_expectedcashflow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='liquidated_date',
            field=models.DateField(blank=True, null=True, verbose_name='data da liquidação'),
        ),
    ]