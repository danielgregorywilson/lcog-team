# Generated by Django 4.0.1 on 2023-03-01 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mainsite', '0004_state_zipcode_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10)),
                ('meal_type', models.CharField(blank=True, choices=[('hot', 'hot'), ('cold', 'cold')], default='hot', max_length=4)),
                ('waitlist', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=100)),
                ('phone_notes', models.CharField(blank=True, max_length=300)),
                ('notes', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.city')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.route')),
                ('zip_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainsite.zipcode')),
            ],
            options={
                'ordering': ['address'],
            },
        ),
    ]