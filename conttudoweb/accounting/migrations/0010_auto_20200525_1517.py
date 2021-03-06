# Generated by Django 3.0.5 on 2020-05-25 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20200523_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialMovement',
            fields=[
            ],
            options={
                'verbose_name': 'movimento financeiro',
                'verbose_name_plural': 'movimentos financeiros',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounting.account',),
        ),
        migrations.AlterModelOptions(
            name='account',
            options={},
        ),
        migrations.AlterField(
            model_name='account',
            name='due_date',
            field=models.DateField(null=True, verbose_name='data de vencimento'),
        ),
        migrations.AlterField(
            model_name='account',
            name='expected_deposit_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.DepositAccount', verbose_name='conta financeira'),
        ),
        migrations.AlterField(
            model_name='account',
            name='liquidated_date',
            field=models.DateField(null=True, verbose_name='data da liquidação'),
        ),
    ]
