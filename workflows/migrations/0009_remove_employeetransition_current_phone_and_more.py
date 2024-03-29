# Generated by Django 4.1.7 on 2023-05-23 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0008_employeetransition_computer_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeetransition',
            name='current_phone',
        ),
        migrations.AddField(
            model_name='employeetransition',
            name='cell_phone',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeetransition',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='employeetransition',
            name='cubicle_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
