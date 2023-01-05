from dataclasses import dataclass
import datetime
from time import time

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from mainsite.helpers import is_true_string

from people.models import Employee

from timeoff.helpers import (
    send_employee_manager_acknowledged_timeoff_request_notification,
    send_manager_new_timeoff_request_notification
)
from workflows.models import (
    Process, ProcessInstance, Role, Step, StepChoice, StepInstance, Workflow,
    WorkflowInstance
)

from workflows.serializers import (
    ProcessInstanceSerializer, ProcessSerializer, RoleSerializer,
    StepChoiceSerializer, StepInstanceSerializer, StepSerializer,
    WorkflowInstanceSerializer, WorkflowSerializer
)


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]

    def get_queryset(self):
        """

        """
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                instances = Workflow.objects.all()
            else:
                instances = Workflow.objects.none()
            return instances

    # def create(self, request):
    #     if 'from' in request.data['dates']:
    #         start_date = request.data['dates']['from'].replace('/', '-')
    #         end_date = request.data['dates']['to'].replace('/', '-')
    #     else:
    #         start_date = request.data['dates'].replace('/', '-')
    #         end_date = request.data['dates'].replace('/', '-')
    #     note = request.data['note']
    #     employee = request.user.employee
    #     timeoffrequest = TimeOffRequest.objects.create(start_date=start_date, end_date=end_date, note=note, employee=employee)
    #     send_manager_new_timeoff_request_notification(timeoffrequest)
    #     serialized_timeoffrequest = TimeOffRequestSerializer(timeoffrequest,
    #         context={'request': request})
    #     return Response(serialized_timeoffrequest.data)

    # def update(self, request, pk=None):
    #     tor = TimeOffRequest.objects.get(pk=pk)
    #     if 'from' in request.data['dates']:
    #         start_date = request.data['dates']['from'].replace('/', '-')
    #         end_date = request.data['dates']['to'].replace('/', '-')
    #     else:
    #         start_date = request.data['dates'].replace('/', '-')
    #         end_date = request.data['dates'].replace('/', '-')
    #     tor.note = request.data['note']
    #     if start_date != str(tor.start_date) or end_date != str(tor.end_date):
    #         tor.start_date = start_date
    #         tor.end_date = end_date
    #         tor.acknowledged = None # Reset acknowledged status since we are making a change
    #     tor.save()
    #     serialized_tor = TimeOffRequestSerializer(tor,
    #         context={'request': request})
    #     return Response(serialized_tor.data)
    
    # def partial_update(self, request, pk=None):
    #     """
    #     Acknowledge a time off request.
    #     """
    #     tor = TimeOffRequest.objects.get(pk=pk)
    #     tor.acknowledged = request.data['acknowledged']
    #     tor.save()
    #     send_employee_manager_acknowledged_timeoff_request_notification(tor)
    #     serialized_tor = TimeOffRequestSerializer(tor,
    #         context={'request': request})
    #     return Response(serialized_tor.data)


class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    queryset = WorkflowInstance.objects.all()
    serializer_class = WorkflowInstanceSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]

    # def get_queryset(self):
    #     """

    #     """
    #     user = self.request.user
    #     if user.is_authenticated:
    #         action_required = self.request.query_params.get('action_required',
    #             None)
    #         complete = self.request.query_params.get('complete', None)
    #         if action_required is not None and is_true_string(action_required):
    #             queryset = WorkflowInstance.action_required.get_queryset(user)
            
            
    #         if user.is_superuser:
    #             instances = WorkflowInstance.objects.all()
    #         else:
    #             instances = WorkflowInstance.objects.none()
    #         return instances

    # def create(self, request):
    #     if 'from' in request.data['dates']:
    #         start_date = request.data['dates']['from'].replace('/', '-')
    #         end_date = request.data['dates']['to'].replace('/', '-')
    #     else:
    #         start_date = request.data['dates'].replace('/', '-')
    #         end_date = request.data['dates'].replace('/', '-')
    #     note = request.data['note']
    #     employee = request.user.employee
    #     timeoffrequest = TimeOffRequest.objects.create(start_date=start_date, end_date=end_date, note=note, employee=employee)
    #     send_manager_new_timeoff_request_notification(timeoffrequest)
    #     serialized_timeoffrequest = TimeOffRequestSerializer(timeoffrequest,
    #         context={'request': request})
    #     return Response(serialized_timeoffrequest.data)

    # def update(self, request, pk=None):
    #     tor = TimeOffRequest.objects.get(pk=pk)
    #     if 'from' in request.data['dates']:
    #         start_date = request.data['dates']['from'].replace('/', '-')
    #         end_date = request.data['dates']['to'].replace('/', '-')
    #     else:
    #         start_date = request.data['dates'].replace('/', '-')
    #         end_date = request.data['dates'].replace('/', '-')
    #     tor.note = request.data['note']
    #     if start_date != str(tor.start_date) or end_date != str(tor.end_date):
    #         tor.start_date = start_date
    #         tor.end_date = end_date
    #         tor.acknowledged = None # Reset acknowledged status since we are making a change
    #     tor.save()
    #     serialized_tor = TimeOffRequestSerializer(tor,
    #         context={'request': request})
    #     return Response(serialized_tor.data)
    
    # def partial_update(self, request, pk=None):
    #     """
    #     Acknowledge a time off request.
    #     """
    #     tor = TimeOffRequest.objects.get(pk=pk)
    #     tor.acknowledged = request.data['acknowledged']
    #     tor.save()
    #     send_employee_manager_acknowledged_timeoff_request_notification(tor)
    #     serialized_tor = TimeOffRequestSerializer(tor,
    #         context={'request': request})
    #     return Response(serialized_tor.data)


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
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
                instances = Process.objects.all()
            else:
                instances = Process.objects.none()
            return instances


class ProcessInstanceViewSet(viewsets.ModelViewSet):
    queryset = ProcessInstance.objects.all()
    serializer_class = ProcessInstanceSerializer
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
                instances = ProcessInstance.objects.all()
            else:
                instances = ProcessInstance.objects.none()
            return instances


class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer
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
                instances = Step.objects.all()
            else:
                instances = Step.objects.none()
            return instances


class StepChoiceViewSet(viewsets.ModelViewSet):
    queryset = StepChoice.objects.all()
    serializer_class = StepChoiceSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]

    # def get_queryset(self):
    #     """
    #     This view should return a list of all time off requests for which
    #     the currently authenticated user is the manager.
    #     """
    #     user = self.request.user
    #     if user.is_authenticated:
    #         if user.is_superuser:
    #             instances = Step.objects.all()
    #         else:
    #             instances = Step.objects.none()
    #         return instances


class StepInstanceViewSet(viewsets.ModelViewSet):
    queryset = StepInstance.objects.all()
    serializer_class = StepInstanceSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]

    # def get_queryset(self):
    #     """
    #     This view should return a list of all time off requests for which
    #     the currently authenticated user is the manager.
    #     """
    #     user = self.request.user
    #     if user.is_authenticated:
    #         if user.is_superuser:
    #             instances = StepInstance.objects.all()
    #         else:
    #             instances = StepInstance.objects.none()
    #         return instances
    
    def partial_update(self, request, pk=None):
        """
        Complete a step instance
        """
        # Complete the current step instance
        stepinstance = StepInstance.objects.get(pk=pk)
        stepinstance.completed_at = timezone.now()
        stepinstance.completed_by = request.user.employee
        stepinstance.save()
        
        # TODO: Do anything that needs to be done to prep the next step like email people

        processinstance = stepinstance.process_instance

        # Update the process instance
        if stepinstance.step.end:
            # If this is the last step instance in a process, complete the process
            processinstance.completed_at = timezone.now()
            processinstance.current_step_instance = None
        else:
            # Make the next StepInstance
            if 'nextStepPk' in request.data:
                next_step = Step.objects.get(pk=request.data['nextStepPk'])
            else:
                next_step=stepinstance.step.next_step
            new_stepinstance = StepInstance.objects.create(
                step=next_step,
                process_instance=processinstance
            )
            processinstance.current_step_instance = new_stepinstance
        processinstance.save()

        serialized_stepinstance = StepInstanceSerializer(stepinstance,
            context={'request': request})
        return Response(serialized_stepinstance.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
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
                instances = Role.objects.all()
            else:
                instances = Role.objects.none()
            return instances