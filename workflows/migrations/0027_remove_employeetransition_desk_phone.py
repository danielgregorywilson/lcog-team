# Generated by Django 4.2.11 on 2024-10-08 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0026_alter_processinstance_workflow_instance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetransition',
            name='desk_phone',
        ),
    ]
