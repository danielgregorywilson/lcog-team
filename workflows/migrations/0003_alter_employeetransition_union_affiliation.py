# Generated by Django 4.0.1 on 2023-02-21 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0002_remove_employeetransition_new_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetransition',
            name='union_affiliation',
            field=models.CharField(choices=[('N', 'Non-Represented'), ('E', 'EA'), ('S', 'SEIU'), ('M', 'Management')], max_length=2),
        ),
    ]
