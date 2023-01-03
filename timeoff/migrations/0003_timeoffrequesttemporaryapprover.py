# Generated by Django 4.0.1 on 2022-12-28 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0044_employee_email_opt_out_all_and_more'),
        ('timeoff', '0002_timeoffrequest_private_note_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeOffRequestTemporaryApprover',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('employee_in_stead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_off_request_approvers_in_stead', to='people.employee')),
                ('employee_on_leave', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_off_request_approvers_on_leave', to='people.employee')),
            ],
        ),
    ]