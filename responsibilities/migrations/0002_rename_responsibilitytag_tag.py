# Generated by Django 4.0.1 on 2022-03-08 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('responsibilities', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ResponsibilityTag',
            new_name='Tag',
        ),
    ]