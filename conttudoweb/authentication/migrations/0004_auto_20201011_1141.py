# Generated by Django 3.1.2 on 2020-10-11 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_group_permission_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'perfil de acesso', 'verbose_name_plural': 'perfis de acesso'},
        ),
    ]
