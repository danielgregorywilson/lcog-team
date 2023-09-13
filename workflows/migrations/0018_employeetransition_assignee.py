# Generated by Django 4.2.4 on 2023-09-13 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0017_employeetransition_fiscal_field_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeetransition',
            name='assignee',
            field=models.CharField(choices=[('None', 'None'), ('Submitter', 'Submitter'), ('Hiring Lead', 'Hiring Lead'), ('Fiscal', 'Fiscal'), ('HR', 'HR'), ('Complete', 'Complete')], default='None', max_length=100),
        ),
    ]
