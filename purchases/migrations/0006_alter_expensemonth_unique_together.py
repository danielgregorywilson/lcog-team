# Generated by Django 4.2.11 on 2024-10-17 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0052_employee_email_opt_out_workflows_processes'),
        ('purchases', '0005_expensemonthlock'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expensemonth',
            unique_together={('purchaser', 'month', 'year', 'card')},
        ),
    ]
