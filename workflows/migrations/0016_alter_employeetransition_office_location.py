# Generated by Django 4.1.7 on 2023-08-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0015_employeetransition_lwop_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetransition',
            name='office_location',
            field=models.CharField(blank=True, choices=[('Cottage Grove', 'Cottage Grove'), ('Florence', 'Florence'), ('Junction City', 'Junction City'), ('Oakridge', 'Oakridge'), ('PPB - 1st Floor', 'PPB - 1st Floor'), ('PPB - 4th Floor', 'PPB - 4th Floor'), ('PPB - 5th Floor', 'PPB - 5th Floor'), ('Schaefers - Basement', 'Schaefers - Basement'), ('Schaefers - 1st Floor', 'Schaefers - 1st Floor'), ('Schaefers - 2nd Floor', 'Schaefers - 2nd Floor'), ('Schaefers - 3rd Floor', 'Schaefers - 3rd Floor'), ('Senior Meals Site', 'Senior Meals Site'), ('Veneta', 'Veneta')], max_length=30),
        ),
    ]
