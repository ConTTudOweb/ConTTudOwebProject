# Generated by Django 3.0.5 on 2020-05-23 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_auto_20200523_1448'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'movimento financeiro', 'verbose_name_plural': 'movimentos financeiros'},
        ),
        migrations.RemoveField(
            model_name='account',
            name='reconciled',
        ),
        migrations.AddField(
            model_name='account',
            name='liquidated_date',
            field=models.DateField(blank=True, null=True, verbose_name='data da liquidação'),
        ),
    ]
