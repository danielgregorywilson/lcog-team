# Generated by Django 4.2.7 on 2024-01-11 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0047_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performancereview',
            name='action_other',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='action other'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='evaluation_comments_employee',
            field=models.TextField(blank=True, default='', verbose_name='employee comments'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='evaluation_goals_employee',
            field=models.TextField(blank=True, default='', verbose_name='goals for the coming year (employee)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='evaluation_goals_manager',
            field=models.TextField(blank=True, default='', verbose_name='goals for the coming year (manager)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='evaluation_opportunities',
            field=models.TextField(blank=True, default='', verbose_name='opportunities for growth'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='performancereview',
            name='evaluation_successes',
            field=models.TextField(blank=True, default='', verbose_name="employee's successes"),
            preserve_default=False,
        ),
    ]
