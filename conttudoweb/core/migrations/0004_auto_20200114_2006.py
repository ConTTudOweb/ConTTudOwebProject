# Generated by Django 3.0.2 on 2020-01-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_people_state_subscription_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='name',
            field=models.CharField(max_length=60, unique=True, verbose_name='nome'),
        ),
    ]