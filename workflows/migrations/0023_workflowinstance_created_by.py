# Generated by Django 4.2.11 on 2024-05-04 00:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0050_workflowoptions_employee_workflow_options'),
        ('workflows', '0022_workflow_icon_workflow_type_alter_workflow_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflowinstance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='people.employee'),
        ),
    ]