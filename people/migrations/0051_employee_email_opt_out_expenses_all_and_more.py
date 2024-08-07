# Generated by Django 4.2.11 on 2024-07-19 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0050_workflowoptions_employee_workflow_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email_opt_out_expenses_all',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employee',
            name='email_opt_out_workflows_all',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employee',
            name='email_opt_out_workflows_transitions',
            field=models.BooleanField(default=False),
        ),
    ]
