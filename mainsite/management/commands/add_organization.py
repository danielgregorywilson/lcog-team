import json
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from mainsite.models import Organization
from people.models import Employee, JobTitle


class Command(BaseCommand):
    help = "Add an Organization from a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            'json_file',
            type=str,
            help="Path to the JSON file containing organization data."
        )

    def handle(self, *args, **options):
        json_file_path = options['json_file']

        try:
            # Load and parse the JSON file
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

            # Validate required fields in the JSON
            if 'name' not in data or 'employees' not in data:
                raise CommandError(
                    "JSON file must contain 'name' and 'employees' fields."
                )

            # Create or get the Organization
            organization_name = data['name']
            organization_description = data.get('description', '')
            organization, created = Organization.objects.get_or_create(
                name=organization_name,
                defaults={'description': organization_description}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created Organization: {organization_name}"
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f"Organization '{organization_name}' already exists."
                ))

            # Process each employee in the JSON
            for employee_data in data['employees']:
                # Parse first and last names from the 'name' field
                full_name = employee_data.get('name', '')
                if not full_name:
                    self.stdout.write(self.style.WARNING(
                        "Skipping employee with missing 'name' field."
                    ))
                    continue

                name_parts = full_name.split()
                first_name = name_parts[0]
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 \
                    else ''

                # Get email and position
                email = employee_data.get('email', '')
                position = employee_data.get('position', '')
                # Get or create the JobTitle
                job_title, job_title_created = JobTitle.objects.get_or_create(
                    name=position
                )
                if job_title_created:
                    self.stdout.write(
                        self.style.WARNING(f"Created JobTitle: {position}")
                    )

                if not email:
                    self.stdout.write(self.style.WARNING(
                        f"Skipping employee '{full_name}' with missing " +
                            "'email' field."
                    ))
                    continue

                # Create or get the User
                user, user_created = User.objects.get_or_create(
                    username=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email
                    }
                )
                if user_created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created User: {email}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"User '{email}' already exists.")
                    )

                # Create or get the Employee
                employee, employee_created = Employee.objects.get_or_create(
                    user=user,
                    defaults={
                        'organization': organization,
                        'active': True,
                        'job_title': job_title
                    }
                )
                if employee_created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created Employee for User: {email}"
                    ))
                else:
                    self.stdout.write(self.style.WARNING(
                        f"Employee for User '{email}' already exists."
                    ))

        except FileNotFoundError:
            raise CommandError(f"File '{json_file_path}' does not exist.")
        except json.JSONDecodeError:
            raise CommandError(
                f"File '{json_file_path}' is not a valid JSON file."
            )
        except Exception as e:
            raise CommandError(f"An error occurred: {e}")

        self.stdout.write(self.style.SUCCESS(
            "Organization and Employees successfully added."
        ))