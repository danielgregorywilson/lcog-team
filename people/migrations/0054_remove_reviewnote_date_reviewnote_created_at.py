# Generated by Django 4.2.11 on 2025-02-01 01:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0053_remove_reviewnote_manager_reviewnote_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewnote',
            name='date',
        ),
        migrations.AddField(
            model_name='reviewnote',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='review note date'),
            preserve_default=False,
        ),
    ]
