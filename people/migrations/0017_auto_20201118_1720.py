# Generated by Django 3.0.7 on 2020-11-19 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0016_auto_20201030_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performancereview',
            name='status',
            field=models.CharField(choices=[('N', 'Needs evaluation'), ('EW', 'Evaluation written and reviewed with employee'), ('EA', 'Evaluation approved up to division director'), ('EP', 'Evaluation processed by HR'), ('ED', 'Evaluation approved by executive director')], default='N', max_length=2, verbose_name='review status'),
        ),
        migrations.AlterField(
            model_name='signature',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='signature date'),
        ),
        migrations.CreateModel(
            name='SignatureReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='most recent reminder date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Employee')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.PerformanceReview', verbose_name='performance review')),
            ],
            options={
                'verbose_name': 'Most Recent Signature Reminder',
                'verbose_name_plural': 'Most Recent Signature Reminders',
            },
        ),
    ]
