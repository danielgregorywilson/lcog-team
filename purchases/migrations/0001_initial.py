# Generated by Django 4.2.11 on 2024-07-11 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0050_workflowoptions_employee_workflow_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approver_approved', 'Approver Approved'), ('approver_denied', 'Approver Denied'), ('director_approved', 'Director Approved'), ('director_denied', 'Director Denied'), ('fiscal_approved', 'Fiscal Approved'), ('fiscal_denied', 'Fiscal Denied')], default='draft', max_length=17)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=511)),
                ('vendor', models.CharField(blank=True, max_length=255)),
                ('job', models.CharField(blank=True, max_length=255)),
                ('receipt', models.FileField(blank=True, null=True, upload_to='uploads/expenses', verbose_name='receipt')),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ExpenseCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last4', models.IntegerField()),
                ('shared', models.BooleanField(default=False)),
                ('requires_director_approval', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_cards', to='people.employee')),
                ('director', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver_of_cards', to='people.employee')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ExpenseStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statements', to='purchases.expensecard')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='PurchaseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Purchase categories',
            },
        ),
        migrations.CreateModel(
            name='PurchaseObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchases.purchasecategory')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('members', models.ManyToManyField(blank=True, related_name='purchase_roles', to='people.employee')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('gl_code', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('requested', 'Requested'), ('cancelled', 'Cancelled'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('ordered', 'Ordered'), ('received', 'Received'), ('complete', 'Complete')], max_length=255, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_request_created_by', to='people.employee')),
                ('purchase_object', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchases.purchaseobject')),
                ('request_for', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_request_for', to='people.employee')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchase_request_updated_by', to='people.employee')),
            ],
        ),
        migrations.AddField(
            model_name='purchasecategory',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='purchases.role'),
        ),
        migrations.CreateModel(
            name='ExpenseStatementItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Transaction Date')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='purchases.expensestatement')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ExpenseMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approver_approved', 'Approver Approved'), ('approver_denied', 'Approver Denied'), ('director_approved', 'Director Approved'), ('director_denied', 'Director Denied'), ('fiscal_approved', 'Fiscal Approved'), ('fiscal_denied', 'Fiscal Denied')], default='draft', max_length=17)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('submitter_note', models.TextField(blank=True)),
                ('director_approved', models.BooleanField(default=False)),
                ('director_approved_at', models.DateTimeField(blank=True, null=True)),
                ('director_note', models.TextField(blank=True)),
                ('fiscal_approved_at', models.DateTimeField(blank=True, null=True)),
                ('fiscal_note', models.TextField(blank=True)),
                ('card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_months', to='purchases.expensecard')),
                ('fiscal_approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approver_of_expense_month', to='people.employee')),
                ('purchaser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_months', to='people.employee')),
            ],
            options={
                'ordering': ['pk'],
                'unique_together': {('purchaser', 'month', 'year')},
            },
        ),
        migrations.CreateModel(
            name='ExpenseGL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('approver_note', models.TextField(blank=True)),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_gls', to='people.employee')),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gls', to='purchases.expense')),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='expense',
            name='month',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='purchases.expensemonth'),
        ),
    ]
