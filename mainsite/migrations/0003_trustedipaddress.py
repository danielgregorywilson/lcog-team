# Generated by Django 4.0.1 on 2022-04-26 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_alter_imageupload_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrustedIPAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.GenericIPAddressField()),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Trusted IP Address',
                'verbose_name_plural': 'Trusted IP Addresses',
            },
        ),
    ]