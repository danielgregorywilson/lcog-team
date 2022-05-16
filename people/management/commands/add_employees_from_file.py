import csv

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models.manager import Manager

from people.models import Division, Employee, JobTitle, UnitOrProgram

class Command(BaseCommand):
    help = 'Imports employees after exporting from Caselle'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        # Set up database if new
        if not Division.objects.filter(name='Administrative Services').count():
            d = Division.objects.create(name='Administrative Services')
            UnitOrProgram.objects.create(name='-', division=d)
            UnitOrProgram.objects.create(name='Administration', division=d)
        if not Division.objects.filter(name='Government Services').count():
            d = Division.objects.create(name='Government Services')
            UnitOrProgram.objects.create(name='-', division=d)
            UnitOrProgram.objects.create(name='Business Services', division=d)
            UnitOrProgram.objects.create(name='GIS', division=d)
            UnitOrProgram.objects.create(name='Information Services', division=d)
            UnitOrProgram.objects.create(name='MetroTV Services', division=d)
            UnitOrProgram.objects.create(name='Planning Services', division=d)
            UnitOrProgram.objects.create(name='Technology Services', division=d)
            UnitOrProgram.objects.create(name='Telecom', division=d)
            UnitOrProgram.objects.create(name='Transport Services', division=d)
        if not Division.objects.filter(name='Senior & Disability Services').count():
            d = Division.objects.create(name='Senior & Disability Services')
            UnitOrProgram.objects.create(name='-', division=d)
            UnitOrProgram.objects.create(name='Area Plan', division=d)
            UnitOrProgram.objects.create(name='Senior Meals', division=d)
        if not Division.objects.filter(name='Test Division').count():
            d = Division.objects.create(name='Test Division')
            UnitOrProgram.objects.create(name='-', division=d)
            UnitOrProgram.objects.create(name='Test Unit', division=d)
        
        # Import from file
        path = options['path']
        if not path:
            path = 'people/management/employees.csv'
        
        # Keep track of all emails to deactivate removed employees
        emails_in_file = []

        dataReader = csv.reader(open(path), delimiter=',', quotechar='"')
        for row in dataReader:
            # Parse row data
            last_name = row[0]
            first_name = row[1]
            email = row[2].lower()
            
            emails_in_file.append(email)
            
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
            if department in ['Technology Services', 'Business Services']:
                unit_or_program = UnitOrProgram.objects.get(name=department)
            elif department in ['MetroTV Services', 'MetroTV Services GS']:
                unit_or_program = UnitOrProgram.objects.get(name='MetroTV Services')
            elif department in ['Planning Services', 'Planning Svcs', 'Planning Svcs GS', 'Planning Services GS']:
                unit_or_program = UnitOrProgram.objects.get(name='Planning Services')
            elif department in ['Administration', 'Administration FD', 'Administration GS']:
                unit_or_program = UnitOrProgram.objects.get(name='Administration')
            elif department in ['Senior & Disability Services', 'SDS', 'Senior & Disablility', 'Senior & Disablility Services', 'Senior $ Disability Services', 'Senior & Diability Services', 'S&DS']:
                unit_or_program = UnitOrProgram.objects.get(division__name='Senior & Disability Services', name='-')
            elif department == 'Govt Services':
                unit_or_program = UnitOrProgram.objects.get(division__name='Government Services', name='-')
            elif department in ['Transport Services', 'Transport Service', 'Transport Service GS']:
                unit_or_program = UnitOrProgram.objects.get(name='Transport Services')
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
                updated_title = employee.job_title != job_title
                updated_department = employee.unit_or_program != unit_or_program
                if updated_title or updated_department:
                    if updated_title:
                        employee.job_title = job_title
                        employee.save()
                        self.stdout.write(
                            'Updated employee {} {} title'.format(employee.user.first_name, employee.user.last_name)
                        )
                    if updated_department:
                        employee.unit_or_program = unit_or_program
                        employee.save()
                        self.stdout.write(
                            'Updated employee {} {} department'.format(employee.user.first_name, employee.user.last_name)
                        )
            except Employee.DoesNotExist:
                employee = Employee.objects.create(user=user, job_title=job_title, unit_or_program=unit_or_program)
                self.stdout.write(
                    'Created employee {} {}'.format(employee.user.first_name, employee.user.last_name)
                )

        # Deactivate any employee not in the list
        for employee in Employee.active_objects.all():
            if employee.user.email not in emails_in_file:
                employee.active = False
                employee.save()

        # Add managers
        dataReader = csv.reader(open(path), delimiter=',', quotechar='"')
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
            else:
                manager_last_name = None

            if manager_last_name:
                try:
                    if manager_last_name == 'Wilson':
                        manager = Employee.objects.get(is_executive_director=True)
                    elif manager_last_name == 'Johnson':
                        manager = Employee.objects.get(user__last_name=manager_last_name, user__first_name='Lynn')
                    elif manager_last_name == 'Goodman':
                        manager = Employee.objects.get(user__last_name=manager_last_name, user__first_name='Micah')
                    elif manager_last_name == 'Davies':
                        manager = Employee.objects.get(user__last_name=manager_last_name, user__first_name='Nancy')
                    elif manager_last_name == 'Sheelar2': # WTF
                        manager = Employee.objects.get(user__last_name='Sheelar', user__first_name='Stephanie')
                    elif manager_last_name == 'Newall': # Nicole Wilbur changed last name
                        manager = Employee.objects.get(user__last_name='Wilbur', user__first_name='Nicole')
                    elif manager_last_name == 'Crowder':
                        manager = Employee.objects.get(user__last_name='Crowder', user__first_name='Jordan')
                    elif manager_last_name == 'Wright':
                        manager = Employee.objects.get(user__last_name='Wright', user__first_name='Vicki')
                    elif manager_last_name == 'Sowards': # Sowards doesn't exist
                        manager = Employee.objects.get(user__last_name='Sheelar', user__first_name='Stephanie')
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