# Generated by Django 4.0.1 on 2022-01-28 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0032_responsibility'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='responsibility',
            options={'ordering': ['name'], 'verbose_name': 'Responsibility', 'verbose_name_plural': 'Responsibilities'},
        ),
    ]