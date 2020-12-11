# Generated by Django 3.0.7 on 2020-12-11 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0019_signaturereminder_next_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signaturereminder',
            options={'get_latest_by': 'date', 'verbose_name': 'Signature Reminder', 'verbose_name_plural': 'Signature Reminders'},
        ),
        migrations.AddField(
            model_name='performancereview',
            name='action_other',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='action other'),
        ),
        migrations.AlterField(
            model_name='signaturereminder',
            name='date',
            field=models.DateField(auto_now=True, verbose_name='reminder date'),
        ),
        migrations.AlterField(
            model_name='signaturereminder',
            name='next_date',
            field=models.DateField(verbose_name='planned next reminder date'),
        ),
    ]
