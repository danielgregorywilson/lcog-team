# Generated by Django 4.2.11 on 2024-10-28 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0006_alter_expensemonth_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
