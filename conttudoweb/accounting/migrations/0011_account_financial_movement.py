# Generated by Django 3.0.5 on 2020-05-25 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0010_auto_20200525_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='financial_movement',
            field=models.BooleanField(default=False),
        ),
    ]
