# Generated by Django 4.0.1 on 2022-09-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeoff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeoffrequest',
            name='private_note',
            field=models.TextField(blank=True, help_text='Visible only to manager', null=True),
        ),
        migrations.AlterField(
            model_name='timeoffrequest',
            name='note',
            field=models.TextField(blank=True, help_text='Visible to team members', null=True),
        ),
    ]
