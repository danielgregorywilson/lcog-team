# Generated by Django 4.1.7 on 2023-05-04 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0005_alter_employeetransition_office_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetransition',
            name='title',
        ),
        migrations.AlterField(
            model_name='employeetransition',
            name='employee_middle_initial',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
