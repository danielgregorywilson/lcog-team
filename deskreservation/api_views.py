from datetime import date, datetime, timedelta
from pytz import timezone

from django.utils.timezone import get_current_timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Desk, DeskReservation
from .serializers import DeskReservationSerializer, DeskSerializer
from mainsite.helpers import get_is_trusted_ip
from people.models import Employee


class DeskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for desk reservations.
    """
    queryset = Desk.active_objects.all()
    serializer_class = DeskSerializer

    # TODO: We should only allow trusted IPs to see desks unauthenticated,
    # but I couldn't get it to work because the server doesn't have the client
    # IP.
    # def get_queryset(self):
    #     """
    #     Return a list of all desks to any authenticated user.
    #     Optionally filter by building and/or floor.
    #     """
    #     user = self.request.user
    #     is_trusted_ip = get_is_trusted_ip()
    #     if user.is_authenticated or is_trusted_ip:
    #         queryset = Desk.active_objects.all()
    #         building = self.request.query_params.get('building', None)
    #         floor = self.request.query_params.get('floor', None)
    #         if building is not None:
    #             queryset = queryset.filter(building=building)
    #         if floor is not None:
    #             queryset = queryset.filter(floor=floor)
    #     else:
    #         queryset = Desk.objects.none()
    #     return queryset


class DeskReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for desk reservations.
    """
    queryset = DeskReservation.currently_reserved_objects.all()
    serializer_class = DeskReservationSerializer

    # TODO: We should only allow trusted IPs to see reservations
    # unauthenticated, but I couldn't get it to work because the server doesn't
    # have the client IP.
    # def get_queryset(self):
    #     """
    #     Return a list of all desk reservations to any authenticated user.
    #     Optionally filter by employee.
    #     """
    #     user = self.request.user
    #     is_trusted_ip = get_is_trusted_ip()
    #     if user.is_authenticated or is_trusted_ip:
    #         queryset = DeskReservation.currently_reserved_objects.all()
    #         employee = self.request.query_params.get('employee', None)
    #         if employee is not None and employee.isdigit():
    #             queryset = queryset.filter(employee=employee)
    #     else:
    #         queryset = DeskReservation.objects.none()
    #     return queryset


    def create(self, request):
        employee = Employee.objects.get(pk=request.data['employee_pk']) if request.data['employee_pk'] != -1 else None
        desk = Desk.objects.get(number=request.data['desk_number']) if request.data['desk_number'] != -1 else None
        existing_reservations = DeskReservation.objects.filter(desk=desk, check_out__isnull=True)
        if existing_reservations.count():
            # Check to see if the desk is already reserved by someone else.
            serialized_reservation = DeskReservationSerializer(existing_reservations[0],
                context={'request': request})
            return Response({**serialized_reservation.data, 'created': False})
        else:
            if desk.held_today and not any([employee in hold.employees.all() for hold in desk.todays_holds]):
                # Check to see if the desk is held for other employees today.
                return Response({'desk_number': request.data['desk_number'], 'desk_held': True})
            else:
                # Otherwise, reserve the desk
                reservation = DeskReservation.objects.create(employee=employee, desk=desk)
                serialized_reservation = DeskReservationSerializer(reservation,
                    context={'request': request})
                return Response({**serialized_reservation.data, 'created': True})

    @action(detail=True, methods=['put'], url_path='cancel-reservation', url_name='cancel-reservation')
    def cancel_reservation(self, request, pk=None):
        reservation = DeskReservation.objects.get(pk=pk)
        reservation.check_out = datetime.now(tz=get_current_timezone())
        reservation.save()
        serialized_reservation = DeskReservationSerializer(reservation,
            context={'request': request})
        return Response(serialized_reservation.data)
    
    @staticmethod
    def parseReportRequestData(data):
        """
        Helper method to parse the start and end times in a desk reservation
        report request.
        """
        start_date_time = data['startDateTime']
        end_date_time = data['endDateTime']
        # If no date time specified, set to whole of last month
        if not start_date_time:
            today = date.today()
            first_of_this_month = today.replace(day=1)
            last_of_last_month = first_of_this_month - timedelta(days=1)
            first_of_last_month = last_of_last_month.replace(day=1)
            start_date_time = datetime.combine(
                first_of_last_month, datetime.min.time()
            )
        else:
            start_date_time = datetime.strptime(
                start_date_time, '%Y-%m-%d %H:%M'
            )
        if not end_date_time:
            today = date.today()
            first_of_this_month = today.replace(day=1)
            end_date_time = datetime.combine(
                first_of_this_month, datetime.min.time()
            )
        else:
            end_date_time = datetime.strptime(end_date_time, '%Y-%m-%d %H:%M')
        start_date_time = timezone('US/Pacific').localize(start_date_time)
        end_date_time = timezone('US/Pacific').localize(end_date_time)
        return (start_date_time, end_date_time)

    @action(
        detail=False,
        methods=['post'],
        url_path='desk-summary-report',
        url_name='desk-summary-report'
    )
    def desk_summary_report(self, request):
        """
        For each desk, and within the range, give the number of hours it was
        utilized and the number of days it was utilized at all.
        """
        start_date_time, end_date_time = \
            self.parseReportRequestData(request.data)
        desk_stats = {}
        for desk in Desk.objects.all():
            total_hours = timedelta(0)
            days_utilized = []
            most_frequent_employee = '' 
            most_frequent_employee_time = timedelta(0)
            reservations = DeskReservation.objects.filter(
                desk=desk,
                check_in__lte=end_date_time,
                check_out__gte=start_date_time
            )
            for reservation in reservations:
                start = max(start_date_time, reservation.check_in)
                end = min(end_date_time, reservation.check_out)
                reservation_duration = end - start
                total_hours += reservation_duration
                day = [start.month, start.day]
                if not day in days_utilized:
                    days_utilized.append(day)
                if reservation_duration > most_frequent_employee_time:
                    most_frequent_employee_time = reservation_duration
                    most_frequent_employee = reservation.employee.username()
            desk_stats[
                f'{desk.get_building_display()} {desk.floor}F {desk.number}'
            ] = {
                'total_hours': \
                    f'{total_hours.days * 24 + total_hours.seconds // 3600}h' +
                    f'{(total_hours.seconds//60)%60}m',
                'days_utilized': len(days_utilized),
                'most_frequent_employee': most_frequent_employee
            }
        return Response(desk_stats)

    @action(
        detail=False,
        methods=['post'],
        url_path='desk-detail-report',
        url_name='desk-detail-report'
    )
    def desk_detail_report(self, request):
        start_dt, end_dt = self.parseReportRequestData(request.data)
        # For each desk, and within the date range, give all reservations.
        reservation_data = {}
        reservations = DeskReservation.objects.filter(
            check_in__lte=end_dt,
            check_out__gte=start_dt,
            desk__pk__in=request.data['desks']
        )
        for res in reservations:
            start = max(start_dt, res.check_in)
            end = min(end_dt, res.check_out)
            duration = end - start
            reservation_data[res.pk] = {
                'employee': res.employee.username(),
                'desk': f'{res.desk.get_building_display()} {res.desk.floor}' +
                    f'F {res.desk.number}',
                'day': res.check_in.strftime('%Y-%m-%d'),
                'total_hours':
                    f'{duration.days * 24 + duration.seconds // 3600}h' +
                    f'{(duration.seconds//60)%60}m'
            }
        return Response(reservation_data)
    
    @action(
        detail=False,
        methods=['post'],
        url_path='employee-summary-report',
        url_name='employee-summary-report'
    )
    def employee_summary_report(self, request):
        """
        For each desk, and within the range, give the number of hours it was
        utilized and the number of days it was utilized at all.
        """
        start_date_time, end_date_time = \
            self.parseReportRequestData(request.data)
        employee_stats = {}
        for employee in Employee.objects.all():
            total_hours = timedelta(0)
            days_utilized = []
            most_frequent_desk = '' 
            most_frequent_desk_time = timedelta(0)
            reservations = DeskReservation.objects.filter(
                employee=employee,
                check_in__lte=end_date_time,
                check_out__gte=start_date_time
            )
            for reservation in reservations:
                start = max(start_date_time, reservation.check_in)
                end = min(end_date_time, reservation.check_out)
                reservation_duration = end - start
                total_hours += reservation_duration
                day = [start.month, start.day]
                if not day in days_utilized:
                    days_utilized.append(day)
                if reservation_duration > most_frequent_desk_time:
                    most_frequent_desk_time = reservation_duration
                    desk = reservation.desk
                    most_frequent_desk = f'{desk.get_building_display()} ' +\
                        f'{desk.floor}F {desk.number}'
            employee_stats[f'{employee.username()}'] = {
                'total_hours':
                    f'{total_hours.days * 24 + total_hours.seconds // 3600}h' +
                    f'{(total_hours.seconds//60)%60}m',
                'days_utilized': len(days_utilized),
                'most_frequent_desk': most_frequent_desk
            }
        return Response(employee_stats)

    @action(
        detail=False,
        methods=['post'],
        url_path='employee-detail-report',
        url_name='employee-detail-report'
    )
    def employee_detail_report(self, request):
        start_dt, end_dt = self.parseReportRequestData(request.data)
        # For each employee, and within the date range, give all reservations.
        reservation_data = {}
        reservations = DeskReservation.objects.filter(
            check_in__lte=end_dt,
            check_out__gte=start_dt,
            employee__pk__in=request.data['employees']
        )
        for res in reservations:
            start = max(start_dt, res.check_in)
            end = min(end_dt, res.check_out)
            duration = end - start
            reservation_data[res.pk] = {
                'employee': res.employee.username(),
                'desk': f'{res.desk.get_building_display()} {res.desk.floor}' +
                    f'F {res.desk.number}',
                'day': res.check_in.strftime('%Y-%m-%d'),
                'total_hours':
                    f'{duration.days * 24 + duration.seconds // 3600}h' +
                    f'{(duration.seconds//60)%60}m'
            }
        return Response(reservation_data)
