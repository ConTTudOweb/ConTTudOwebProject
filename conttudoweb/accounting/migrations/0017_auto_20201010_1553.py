# Generated by Django 3.1.2 on 2020-10-10 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0016_auto_20201007_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accountpayable',
            options={'verbose_name': 'conta (à pagar/paga)', 'verbose_name_plural': 'contas (à pagar/pagas)'},
        ),
        migrations.AlterModelOptions(
            name='accountreceivable',
            options={'verbose_name': 'conta (à receber/recebida)', 'verbose_name_plural': 'contas (à receber/recebidas)'},
        ),
    ]