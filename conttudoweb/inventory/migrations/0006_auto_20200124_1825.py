# Generated by Django 3.0.2 on 2020-01-24 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20200118_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='código')),
                ('description', models.CharField(max_length=120, verbose_name='descrição')),
            ],
            options={
                'verbose_name': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='código')),
                ('description', models.CharField(max_length=120, verbose_name='descrição')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.Category')),
            ],
            options={
                'verbose_name': 'subcategoria',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='uubcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.Subcategory'),
        ),
    ]
