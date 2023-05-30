# Generated by Django 4.1.7 on 2023-05-25 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0045_employee_temporary'),
        ('workflows', '0009_remove_employeetransition_current_phone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransitionChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('changes', models.JSONField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.employee')),
                ('transition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='workflows.employeetransition')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
    ]
