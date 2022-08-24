import datetime
from time import time
from responsibilities.models import Responsibility

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from mainsite.helpers import is_true_string

from people.models import Employee

from timeoff.helpers import (
    send_employee_manager_acknowledged_timeoff_request_notification,
    send_manager_new_timeoff_request_notification
)
from timeoff.models import TimeOffRequest

from timeoff.serializers import (
    ConflictingResponsibilitiesSerializer, TimeOffRequestSerializer
)


class TimeOffRequestViewSet(viewsets.ModelViewSet):
    queryset = TimeOffRequest.objects.all()
    serializer_class = TimeOffRequestSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]

    def get_queryset(self):
        """
        This view should return a list of all time off requests for which
        the currently authenticated user is the manager.
        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                requests = TimeOffRequest.objects.all()
            elif 'managed' in self.request.GET and is_true_string(self.request.GET['managed']):
                requests = TimeOffRequest.objects.filter(employee__manager=user.employee)
            elif 'team' in self.request.GET and is_true_string(self.request.GET['team']):
                requests = TimeOffRequest.objects.filter(
                    Q(employee__manager=user.employee.manager) | # Your team members
                    Q(employee=user.employee.manager) | # Your manager
                    Q(employee__manager=user.employee) # Your direct reports
                )
            else:
                requests = TimeOffRequest.objects.filter(employee=user.employee)
            for request in requests:
                request.conflicts = [
                    {
                        'pk': e.pk,
                        'name': e.name,
                        'responsibility_names': e.responsibility_names
                    } for e in request.conflicting_responsibilities
                ]
            return requests

    def create(self, request):
        if 'from' in request.data['dates']:
            start_date = request.data['dates']['from'].replace('/', '-')
            end_date = request.data['dates']['to'].replace('/', '-')
        else:
            start_date = request.data['dates'].replace('/', '-')
            end_date = request.data['dates'].replace('/', '-')
        note = request.data['note']
        employee = request.user.employee
        timeoffrequest = TimeOffRequest.objects.create(start_date=start_date, end_date=end_date, note=note, employee=employee)
        send_manager_new_timeoff_request_notification(timeoffrequest)
        serialized_timeoffrequest = TimeOffRequestSerializer(timeoffrequest,
            context={'request': request})
        return Response(serialized_timeoffrequest.data)

    def update(self, request, pk=None):
        tor = TimeOffRequest.objects.get(pk=pk)
        if 'from' in request.data['dates']:
            start_date = request.data['dates']['from'].replace('/', '-')
            end_date = request.data['dates']['to'].replace('/', '-')
        else:
            start_date = request.data['dates'].replace('/', '-')
            end_date = request.data['dates'].replace('/', '-')
        tor.note = request.data['note']
        if start_date != str(tor.start_date) or end_date != str(tor.end_date):
            tor.start_date = start_date
            tor.end_date = end_date
            tor.acknowledged = None # Reset acknowledged status since we are making a change
        tor.save()
        serialized_tor = TimeOffRequestSerializer(tor,
            context={'request': request})
        return Response(serialized_tor.data)
    
    def partial_update(self, request, pk=None):
        """
        Acknowledge a time off request.
        """
        tor = TimeOffRequest.objects.get(pk=pk)
        tor.acknowledged = request.data['acknowledged']
        tor.save()
        send_employee_manager_acknowledged_timeoff_request_notification(tor)
        serialized_tor = TimeOffRequestSerializer(tor,
            context={'request': request})
        return Response(serialized_tor.data)

    # TODO: Duplicated in TimeOffRequest model property .conflicting_responsibilities. Use a generic helper function to handle both?
    # A list of employees with time off requests in the same time period with
    # shared/backup responsibilities.
    @action(detail=False, methods=['post'])
    def conflicting_responsibilities(self, request):
        dates = request.data['dates']
        if 'from' in dates:
            start_year, start_month, start_day = dates['from'].split('/')
            end_year, end_month, end_day = dates['to'].split('/')
        else:
            start_year, start_month, start_day = dates.split('/')
            end_year, end_month, end_day = start_year, start_month, start_day
        if 'user' in request.data:
            employee = request.data['user'].employee
        else:
            employee = request.user.employee
        
        # Get all the employees that share a responsibility with this employee
        responsibility_buddies = Employee.objects.filter(
            Q(primary_responsibilities__in=employee.secondary_responsibilities.all()) |
            Q(secondary_responsibilities__in=employee.primary_responsibilities.all())
        ).distinct()

        # Get all the time off requests for those employees that conflict with
        # this request.
        conflicting_tors = TimeOffRequest.objects\
            .filter(employee__in=responsibility_buddies)\
            .exclude(employee=employee)\
            .exclude(start_date__gt=datetime.date(int(end_year), int(end_month), int(end_day)))\
            .exclude(end_date__lt=datetime.date(int(start_year), int(start_month), int(start_day)))

        # Prune the buddy list of any employees that don't have any conflicting
        # time off requests, and then annotate them with the list of shared
        # responsibilities.
        # First pass: Remove any responsibility buddies that don't have
        # conflicting time off requests.
        for buddy in responsibility_buddies:
            remove_buddy = True
            for tor in conflicting_tors:
                if tor.employee == buddy:
                    remove_buddy = False
            if remove_buddy:
                responsibility_buddies = responsibility_buddies.exclude(pk=buddy.pk)
        # Second pass: Add the responsibility names to the serialized
        # employees.
        for buddy in responsibility_buddies:
            for tor in conflicting_tors:
                if tor.employee == buddy:
                    conflicting_responsibilities = Responsibility.objects.filter(
                        (Q(primary_employee=employee) & Q(secondary_employee=buddy)) |
                        (Q(secondary_employee=employee) & Q(primary_employee=buddy))
                    )
                    buddy.responsibility_names = [r.name for r in conflicting_responsibilities]

        serializer = ConflictingResponsibilitiesSerializer(responsibility_buddies, many=True,
            context={'request': request})
        return Response(serializer.data)
