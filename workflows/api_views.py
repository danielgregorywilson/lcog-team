from dataclasses import dataclass
from datetime import datetime
from time import time

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from mainsite.helpers import is_true_string

from people.models import Employee, JobTitle, UnitOrProgram

from timeoff.helpers import (
    send_employee_manager_acknowledged_timeoff_request_notification,
    send_manager_new_timeoff_request_notification
)
from workflows.helpers import (
    send_gas_pin_notification_email, send_transition_hr_email,
    send_transition_stn_email
)
from workflows.models import (
    EmployeeTransition, Process, ProcessInstance, Role, Step, StepChoice,
    StepInstance, TransitionChange, Workflow, WorkflowInstance
)

from workflows.serializers import (
    EmployeeTransitionSerializer, ProcessInstanceSerializer, ProcessSerializer,
    RoleSerializer, StepChoiceSerializer, StepInstanceSerializer,
    StepSerializer, TransitionChangeSerializer, WorkflowInstanceSerializer,
    WorkflowInstanceSimpleSerializer, WorkflowSerializer
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

    def get_serializer_class(self):
        simple = self.request.query_params.get('simple', None)
        if simple is not None and is_true_string(simple):
            return WorkflowInstanceSimpleSerializer
        return super().get_serializer_class()

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

    def create(self, request):
        import pdb; pdb.set_trace()
        wf = None
        if request.data['type'] == 'employee_onboarding':
            et = EmployeeTransition.objects.create(type=EmployeeTransition.TRANSITION_TYPE_NEW)
            wf = Workflow.objects.get(name="Employee Onboarding")
        elif request.data['type'] == 'employee_returning':
            et = EmployeeTransition.objects.create(type=EmployeeTransition.TRANSITION_TYPE_RETURN)
            # wf = Workflow.objects.get(name="Employee Returning")
        elif request.data['type'] == 'employee_changing':
            et = EmployeeTransition.objects.create(type=EmployeeTransition.TRANSITION_TYPE_CHANGE)
            # wf = Workflow.objects.get(name="Employee Changing")
        elif request.data['type'] == 'employee_exiting':
            et = EmployeeTransition.objects.create(type=EmployeeTransition.TRANSITION_TYPE_EXIT)
            # wf = Workflow.objects.get(name="Employee Exiting")
        else:
            return Response({'error': 'Invalid workflow type'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create workflow instance
        wfi = WorkflowInstance.objects.create(workflow=wf, transition=et)
        # Create process instances
        for process in wf.processes.filter(workflow_start=True):
            process.create_process_instance(wfi)
        serialized_wfi = WorkflowInstanceSerializer(wfi,
            context={'request': request}
        )
        return Response(serialized_wfi.data)

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

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.transition:
            instance.transition.delete()
        return super().destroy(request, pk)


class EmployeeTransitionViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTransition.objects.all()
    serializer_class = EmployeeTransitionSerializer
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
    #     if self.request.data['type'] == 'new_employee_onboarding':
    #         et = EmployeeTransition.objects.create(type=EmployeeTransition.TRANSITION_TYPE_NEW)
    #         wf = Workflow.objects.get(name="New Employee Onboarding")
    #         wfi = WorkflowInstance.objects.create(workflow=wf, transition=et)
    #         # Create process instances
    #         for process in wf.processes.filter(workflow_start=True):
    #             process.create_process_instance(wfi)
    #         serialized_wfi = WorkflowInstanceSerializer(wfi,
    #             context={'request': request}
    #         )
    #         return Response(serialized_wfi.data)

    def update(self, request, pk=None):
        t = EmployeeTransition.objects.get(pk=pk)

        # Set submitter only the first time the transition is updated
        if not t.submitter:
            submitter = Employee.objects.get(pk=request.data['submitter_pk']) if \
                'submitter_pk' in request.data else None
            t.submitter = submitter
            t.date_submitted = datetime.now(tz=get_current_timezone())

        t.type = request.data['type']
        t.employee_first_name = request.data['employee_first_name']
        t.employee_middle_initial = request.data['employee_middle_initial']
        t.employee_last_name = request.data['employee_last_name']
        t.employee_preferred_name = request.data['employee_preferred_name']
        t.employee_id = request.data['employee_id']
        t.employee_number = request.data['employee_number']
        t.employee_email = request.data['employee_email']
        
        if 'title_pk' in request.data and request.data['title_pk'] != -1:
            t.title = JobTitle.objects.get(pk=request.data['title_pk'])
        else:
            t.title = None

        t.fte = request.data['fte']

        # Only the hiring manager, fiscal, or HR can edit salary fields
        user_is_hiring_manager = request.user.employee == t.manager
        user_is_hr = request.user.employee.is_hr_employee
        user_is_fiscal = request.user.employee.is_fiscal_employee
        user_can_edit_salary = any([
            user_is_hiring_manager, user_is_hr, user_is_fiscal
        ])
        editing_salary_range = all([
            'salary_range' in request.data,
            request.data['salary_range'] != t.salary_range
        ])
        editing_salary_step = all([
            'salary_step' in request.data,
            request.data['salary_step'] != t.salary_step
        ])
        editing_salary = editing_salary_range or editing_salary_step
        if editing_salary and not user_can_edit_salary:
            return Response(
                {
                    'error':
                    'Only the hiring manager, fiscal, or HR can edit salary fields.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if editing_salary and user_can_edit_salary:
            t.salary_range = request.data['salary_range']
            t.salary_step = request.data['salary_step']
        
        t.bilingual = request.data['bilingual']
        t.second_language = request.data['second_language']
        
        # Only the original submitter can edit manager field
        user_is_submitter = request.user.employee == t.submitter
        current_manager = t.manager.pk if t.manager else -1
        editing_manager = all([
            # Manager field is being edited
            'manager_pk' in request.data,
            # Manager field is being changed
            request.data['manager_pk'] != current_manager
        ])
        if editing_manager and not user_is_submitter:
            return Response(
                {
                    'error':
                    'Only the original submitter can edit the manager field.'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        if user_is_submitter:
            if editing_manager and request.data['manager_pk'] != -1:
                t.manager = Employee.objects.get(pk=request.data['manager_pk'])
            else:
                t.manager = None
              
        
        if 'unit_pk' in request.data and request.data['unit_pk'] != -1:
            t.unit = UnitOrProgram.objects.get(pk=request.data['unit_pk'])
        else:
            t.unit = None
        
        if 'transition_date' in request.data:
            t.transition_date = request.data['transition_date']
        else:
            t.transition_date = None

        t.preliminary_hire = request.data['preliminary_hire']
        t.delete_profile = request.data['delete_profile']
        t.office_location = request.data['office_location']
        t.cubicle_number = request.data['cubicle_number']
        t.union_affiliation = request.data['union_affiliation']
        t.teleworking = request.data['teleworking']
        t.computer_type = request.data['computer_type']
        t.computer_gl = request.data['computer_gl']
        t.computer_description = request.data['computer_description']
        t.phone_number = request.data['phone_number']
        t.desk_phone = request.data['desk_phone']
        t.phone_request = request.data['phone_request']
        t.phone_request_data = request.data['phone_request_data']
        t.load_code = request.data['load_code']
        t.cell_phone = request.data['cell_phone']
        t.should_delete = request.data['should_delete']
        t.reassign_to = request.data['reassign_to']
        t.gas_pin_needed = request.data['gas_pin_needed']
        t.business_cards = request.data['business_cards']
        t.prox_card_needed = request.data['prox_card_needed']
        t.prox_card_returned = request.data['prox_card_returned']
        
        if 'access_emails_pk' in request.data and request.data['access_emails_pk'] != -1:
            t.access_emails = Employee.objects.get(pk=request.data['access_emails_pk'])    
        else:
            t.access_emails = None 
        
        t.special_instructions = request.data['special_instructions']
        
        t.save()
        serialized_transition = EmployeeTransitionSerializer(t,
            context={'request': request})
        return Response(serialized_transition.data)
    
    # def partial_update(self, request, pk=None):
    #     """
    #     Acknowledge a time off request.
    #     """
    #     import pdb; pdb.set_trace()
    #     tor = TimeOffRequest.objects.get(pk=pk)
    #     tor.acknowledged = request.data['acknowledged']
    #     tor.save()
    #     send_employee_manager_acknowledged_timeoff_request_notification(tor)
    #     serialized_tor = TimeOffRequestSerializer(tor,
    #         context={'request': request})
    #     return Response(serialized_tor.data)

    @action(detail=True, methods=['post'])
    def send_gas_pin_notification_email(self, request, pk):
        transition = EmployeeTransition.objects.get(pk=pk)
        send_gas_pin_notification_email(
            transition,
            sender_name=request.data['senderName'],
            sender_email=request.data['senderEmail'],
            url=request.data['transition_url'] )
        return Response("Gas PIN notification email sent.")

    @action(detail=True, methods=['post'])
    def send_transition_to_email_list(self, request, pk):
        transition = EmployeeTransition.objects.get(pk=pk)
        if request.data['type'] == 'HR':
            send_transition_hr_email(
                transition,
                extra_message=request.data['extraMessage'],
                sender_name=request.data['senderName'],
                sender_email=request.data['senderEmail'],
                url=request.data['transition_url']
            )
        elif request.data['type'] == 'STN':
            send_transition_stn_email(
                transition,
                update=request.data['update'],
                extra_message=request.data['extraMessage'],
                sender_name=request.data['senderName'],
                url=request.data['transition_url']
            )
        else:
            return Response("Invalid type.", status=status.HTTP_400_BAD_REQUEST)
        return Response("Sent email to staff.")


class TransitionChangeViewSet(viewsets.ModelViewSet):
    queryset = TransitionChange.objects.all()
    serializer_class = TransitionChangeSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly
    # ]


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
        Complete or undo completion of a step instance
        """
        stepinstance = StepInstance.objects.get(pk=pk)

        if (request.data['action'] == 'complete'):
            # Complete the current step instance  
            if stepinstance.completed_at:
                # Prevent completing a step instance twice
                return Response({'error': 'This step instance has already been completed.'}, status=status.HTTP_400_BAD_REQUEST)
      
            stepinstance.completed_at = timezone.now()
            stepinstance.completed_by = request.user.employee
            stepinstance.save()
            
            # TODO: Do anything that needs to be done to prep the next step like email people
            
            # Update the process instance
            processinstance = stepinstance.process_instance
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

            # If step instance completion triggers a new process, start it
            workflow_instance = stepinstance.process_instance.workflow_instance
            if stepinstance.step.trigger_processes.count():
                for process in stepinstance.step.trigger_processes.all():
                    process.create_process_instance(workflow_instance)
        
        else:
            # Undo completion of the current step instance
            if not stepinstance.completed_at:
                # Prevent undoing completion of a step instance that hasn't been completed
                return Response({'error': 'This step instance has not been completed.'}, status=status.HTTP_400_BAD_REQUEST)

            # Undo completion of current SI (user and date)
            stepinstance.completed_at = None
            stepinstance.completed_by = None
            stepinstance.save()

            # Update PI
            processinstance = stepinstance.process_instance
            nextStepInstance = StepInstance.objects.get(pk=request.data['nextStepInstancePk'])
            if nextStepInstance.step.end:
                # If the next step is the last step instance in a process, un-complete the process
                processinstance.completed_at = None
            processinstance.current_step_instance = stepinstance
            processinstance.save()

            # Delete next SI
            nextStepInstance.delete()

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