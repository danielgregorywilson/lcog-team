# Generated by Django 3.2.5 on 2021-09-09 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0029_teleworkapplication'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signature',
            options={'verbose_name': 'PR Signature', 'verbose_name_plural': 'PR Signatures'},
        ),
        migrations.AlterField(
            model_name='teleworkapplication',
            name='status',
            field=models.CharField(choices=[('U', 'Not yet approved'), ('A', 'Approved')], default='U', max_length=1, verbose_name='application status'),
        ),
        migrations.CreateModel(
            name='TeleworkSignature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.SmallIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True, verbose_name='signature date')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.teleworkapplication', verbose_name='telework application')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.employee')),
            ],
            options={
                'verbose_name': 'Telework Signature',
                'verbose_name_plural': 'Telework Signatures',
            },
        ),
    ]
