# Generated by Django 3.0.7 on 2021-02-10 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0021_auto_20201222_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='position_description_link_override',
            field=models.URLField(blank=True, null=True, verbose_name='position description link override'),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='position_description_link',
            field=models.URLField(blank=True, null=True, verbose_name='position description link'),
        ),
    ]
