import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from rest_framework.authtoken.models import Token

from people.models import Division, Employee, JobTitle, UnitOrProgram


class Command(BaseCommand):
    help = 'Activates all employees in the Test Division that get deactivated whenever we do an employee import from Caselle'

    def handle(self, *args, **options):
        division = Division.objects.get(name='Test Division')
        employees = Employee.objects.filter(unit_or_program__division=division)
        for employee in employees:
            employee.active = True
            employee.save()
            self.stdout.write(self.style.SUCCESS(f'Activated {employee.name if employee.name else employee.user.username}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully activated all test users.'))
