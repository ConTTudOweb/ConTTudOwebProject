# Generated by Django 3.0.5 on 2020-05-16 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200114_2006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='federativeunit',
            options={'ordering': ('name',), 'verbose_name': 'unidade federativa'},
        ),
    ]
