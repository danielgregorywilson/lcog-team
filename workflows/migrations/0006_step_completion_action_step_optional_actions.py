# Generated by Django 4.0.1 on 2023-01-30 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0005_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='completion_action',
            field=models.ForeignKey(blank=True, help_text='Action to trigger as this step completes', null=True, on_delete=django.db.models.deletion.SET_NULL, to='workflows.action'),
        ),
        migrations.AddField(
            model_name='step',
            name='optional_actions',
            field=models.ManyToManyField(blank=True, related_name='triggering_steps', to='workflows.Action'),
        ),
    ]
