# Generated by Django 3.0.5 on 2020-05-23 17:48

from django.db import migrations
from django.db.models import Q


def delete_recurrences_not_used(apps, schema_editor):
    Recurrence = apps.get_model('accounting', 'Recurrence')
    Account = apps.get_model('accounting', 'Account')
    recurrences = set(Account.objects.all().values_list('recurrence_key', flat=True))
    recurrences.discard(None)
    Recurrence.objects.filter(~Q(id__in=recurrences)).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20200523_1123'),
    ]

    operations = [
        migrations.RunPython(delete_recurrences_not_used),
    ]
