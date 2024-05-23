# Generated by Django 4.2.11 on 2024-05-23 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0007_expensemonth_approved_at_expensemonth_approver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='gls',
            field=models.JSONField(blank=True, default=list, verbose_name='GL Codes'),
        ),
        migrations.AlterField(
            model_name='expense',
            name='job',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='expense',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
