import csv

from django.core.management.base import BaseCommand

from mainsite.models import City, State, ZipCode
from meals.models import Route, Stop

class Command(BaseCommand):
    help = 'Imports hot meal delivery addresses from a CSV file.'

    def handle(self, *args, **options): 
        # Import from file
        path = 'meals/management/hot-meals.csv'

        dataReader = csv.reader(open(path), delimiter=',', quotechar='"')
        for row in dataReader:
            # Parse row data
            last_name = row[0].strip()
            first_name = row[1].strip()
            address = row[2].strip()
            city_name = row[3].strip()
            zip = row[4].strip()
            directions = row[5].strip()
            phone = row[6].strip()
            phone_notes = row[7].strip()
            route_name = row[8].strip()
            override_lat = float(row[9].strip()) if row[9].strip() else None
            override_long = float(row[10].strip()) if row[10].strip() else None
            
            # Skip rows already imported
            existing_stop = Stop.objects.filter(
                last_name=last_name, first_name=first_name, address=address,
                meal_type='hot', waitlist=False
            )
            if existing_stop.count():
                print(
                    f"Skipping {first_name} {last_name} at {address} because",
                    "it already exists."
                )
                continue

            try:
                route = Route.objects.get(name=route_name)
            except Route.DoesNotExist:
                route = Route.objects.create(name=route_name)
            
            try:
                zip_code = ZipCode.objects.get(code=zip)
            except ZipCode.DoesNotExist:
                zip_code = ZipCode.objects.create(code=zip)
            
            try:
                city = City.objects.get(name=city_name)
            except City.DoesNotExist:
                city = City.objects.create(
                    name=city_name, state=State.objects.get(name='Oregon')
                )
            
            try:
                if override_lat:
                     stop = Stop.objects.create(
                        first_name=first_name, last_name=last_name,
                        address=address, city=city, zip_code=zip_code,
                        phone=phone, phone_notes=phone_notes, notes=directions,
                        route=route, latitude=override_lat,
                        longitude=override_long
                    )
                else:
                    stop = Stop.objects.create(
                        first_name=first_name, last_name=last_name,
                        address=address, city=city, zip_code=zip_code,
                        phone=phone, phone_notes=phone_notes,
                        notes=directions, route=route
                    )
                if stop.latitude == 0:
                    if override_lat:
                        stop.latitude = override_lat
                        stop.save()
                    else:
                        print('No override lat')
                        import pdb; pdb.set_trace();
                if stop.longitude == 0:
                    if override_long:
                        stop.longitude = override_long
                        stop.save()
                    else:
                        print('No override long')
                        import pdb; pdb.set_trace();
                print(
                    f"Added {first_name} {last_name} at {address} to",
                    f"route {route}."
                )
            except Exception as e:
                print(e)
                import pdb; pdb.set_trace()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully imported addresses.')
        )