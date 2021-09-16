import csv
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models.manager import Manager

from people.models import Employee, JobTitle, PerformanceReview, UnitOrProgram

class Command(BaseCommand):
    help = 'Sends reminder emails for in-progress performance reviews'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **options):
        path = options['path']
        if not path:
            path = 'people/management/reviews.csv'
        
        dataReader = csv.reader(open(path), delimiter=',', quotechar='"')
        employee_review_rows = [] # Initialize
        for row in dataReader:
            # Parse row data
            if len(row):
                if row[0] in ['Employee Name', 'Notes: ', '04/19/2019 12:50 PM - clid1559"']:
                    continue
                if row[0]:
                    # Check review rows for the previous employee
                    if len(employee_review_rows):
                        self.check_review_rows(employee_review_rows, employee)

                    # Start a new employee section
                    parts = row[0].split(',')
                    last_name = parts[0]
                    first_name = parts[1].strip().split(' ')[0]
                    try:
                        employee = Employee.objects.get(user__last_name=last_name, user__first_name__startswith=first_name)
                    except Employee.DoesNotExist:
                        # If the employee is not otherwise in the system, ignore them
                        continue
                    employee_review_rows = []
                elif row[1] and row[1].split(' ')[0] == 'PR':
                    if row[4] and not row[9]:
                        row[9] = datetime.datetime.strftime(datetime.datetime.strptime(row[4], '%m/%d/%Y') + datetime.timedelta(days=365), '%m/%d/%Y')
                    employee_review_rows += [row]
        
        self.stdout.write(self.style.SUCCESS('Successfully imported reviews.'))

    def check_review_rows(self, rows, employee):
        # Get the most recent review
        sorted_rows = sorted(rows, key=lambda row: datetime.datetime.strptime(row[9], '%m/%d/%Y'))
        most_recent_row = sorted_rows[-1]
        
        # Get the most recent review information
        review_date = datetime.datetime.strptime(most_recent_row[4], '%m/%d/%Y')
        next_review_date = datetime.datetime.strptime(most_recent_row[9], '%m/%d/%Y')
        try:   
            existing_reviews = PerformanceReview.objects.filter(employee=employee).exists()
            if not existing_reviews:
                # review_range = next_review_date - review_date
                if len(rows) > 1:
                    evaluation_type = PerformanceReview.ANNUAL_EVALUATION
                else:
                    evaluation_type = PerformanceReview.PROBATIONARY_EVALUATION
                PerformanceReview.objects.create(
                    employee=employee,
                    period_start_date=review_date,
                    period_end_date=next_review_date,
                    effective_date=next_review_date + datetime.timedelta(days=1),
                    evaluation_type=evaluation_type
                )
                self.stdout.write(
                    'Created review for employee {} {} for period {} - {}'.format(employee.user.first_name, employee.user.last_name, review_date, next_review_date)
                )
                
        except PerformanceReview.DoesNotExist:
            pass

