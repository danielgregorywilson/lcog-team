import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models.manager import Manager

from people.models import Employee, JobTitle, UnitOrProgram

class Command(BaseCommand):
    help = 'Sends reminder emails for in-progress performance reviews'

    def handle(self, *args, **options):
        dataReader = csv.reader(open('people/management/employees.csv'), delimiter=',', quotechar='"')
        for row in dataReader:
            # Parse row data
            last_name = row[0]
            first_name = row[1]
            email = row[2].lower()
            
            title = row[3]
            job_title = JobTitle.objects.get_or_create(name=title)[0]
            
            department_col_pieces = row[4].split(' ')
            if department_col_pieces[0] == 'PR':
                department_col_pieces = department_col_pieces[1:]
            if department_col_pieces[-1] == 'Admin':
                department_col_pieces = department_col_pieces[0:-1]
            if len(department_col_pieces) == 1:
                department = row[4]
            else:
                department = " ".join(department_col_pieces[0:-1])
            department = department.strip()
            if department in ['Technology Services', 'MetroTV Services', 'Planning Services', 'Administration', 'Business Services', 'Transport Services']:
                unit_or_program = UnitOrProgram.objects.get(name=department)
            elif department == 'Planning Svcs':
                unit_or_program = UnitOrProgram.objects.get(name='Planning Services')
            elif department == 'Administration FD':
                unit_or_program = UnitOrProgram.objects.get(name='Administration')
            elif department in ['Senior & Disability Services', 'SDS', 'Senior & Disablility', 'Senior & Disablility Services', 'Senior $ Disability Services', 'Senior & Diability Services']:
                unit_or_program = UnitOrProgram.objects.get(division__name='Senior & Disability Services', name='-')
            elif department == 'Govt Services':
                unit_or_program = UnitOrProgram.objects.get(division__name='Government Services', name='-')
            else:
                raise ValueError('Unknown department {}'.format(department))

            # Get or create user by email. Update user names if necessary.
            try:
                user = User.objects.get(email=email)
                if user.first_name != first_name or user.last_name != last_name:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    self.stdout.write(
                        'Updated user {} {} name'.format(user.first_name, user.last_name)
                    )
            except User.DoesNotExist:
                user = User.objects.create(email=email, username=email.split('@')[0], first_name=first_name, last_name=last_name,)
                self.stdout.write(
                    'Created user {} {}'.format(user.first_name, user.last_name)
                )
                
            # Get or create employee. Update employee department if necessary.
            try:
                employee = Employee.objects.get(user=user)
                if employee.job_title != job_title or employee.unit_or_program != unit_or_program:
                    employee.job_title = job_title
                    employee.unit_or_program = unit_or_program
                    employee.save()
                    self.stdout.write(
                        'Updated employee {} {} title or department'.format(employee.user.first_name, employee.user.last_name)
                    )
            except Employee.DoesNotExist:
                employee = Employee.objects.create(user=user, job_title=job_title, unit_or_program=unit_or_program)
                self.stdout.write(
                    'Created employee {} {}'.format(employee.user.first_name, employee.user.last_name)
                )

        # Add managers
        dataReader = csv.reader(open('people/management/employees.csv'), delimiter=',', quotechar='"')
        for row in dataReader:
            email = row[2].lower()
            user = User.objects.get(email=email)
            employee = Employee.objects.get(user=user)
            department_col_pieces = row[4].split(' ')
            if department_col_pieces[0] == 'PR':
                department_col_pieces = department_col_pieces[1:]
            if department_col_pieces[-1] == 'Admin':
                department_col_pieces = department_col_pieces[0:-1]
            if len(department_col_pieces) > 1:
                manager_last_name = department_col_pieces[-1]

            if manager_last_name:
                try:
                    if manager_last_name == 'Wilson':
                        manager = Employee.objects.get(is_executive_director=True)
                    elif manager_last_name == 'Johnson':
                        manager = Employee.objects.get(user__last_name=manager_last_name, user__first_name='Lynn')
                    elif manager_last_name == 'Goodman':
                        manager = Employee.objects.get(user__last_name=manager_last_name, user__first_name='Micah')
                    else:
                        manager = Employee.objects.get(user__last_name=manager_last_name)
                    if employee.manager != manager:
                        employee.manager = manager
                        employee.save()
                        self.stdout.write(
                            'Added manager {} {} for employee {} {}'.format(manager.user.first_name, manager.user.last_name, employee.user.first_name, employee.user.last_name)
                        )
                except Employee.DoesNotExist:
                    pass
        
        self.stdout.write(self.style.SUCCESS('Successfully imported users.'))