# Generated by Django 3.0.7 on 2021-06-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0025_auto_20210210_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='viewed_security_message',
            field=models.BooleanField(default=False, verbose_name='has viewed security message'),
        ),
    ]
