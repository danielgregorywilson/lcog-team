import datetime
from responsibilities.models import Responsibility

from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import (
    BasePermission, DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated,
    IsAuthenticatedOrReadOnly, SAFE_METHODS
)
from rest_framework.response import Response

from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from mainsite.helpers import (
is_true_string, send_evaluation_written_email_to_employee,
send_signature_email_to_manager
)

from people.models import Employee

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
            if 'managed' in self.request.GET and is_true_string(self.request.GET['managed']):
                return TimeOffRequest.objects.filter(employee__manager=user.employee)
            elif 'team' in self.request.GET and is_true_string(self.request.GET['team']):
                return TimeOffRequest.objects.filter(employee__manager=user.employee.manager)
            else:
                return TimeOffRequest.objects.filter(employee=user.employee)

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
        serialized_timeoffrequest = TimeOffRequestSerializer(timeoffrequest,
            context={'request': request})
        return Response(serialized_timeoffrequest.data)

    # def retrieve(self, request, pk=None):
    #     queryset = PerformanceReview.objects.all()
    #     pr = get_object_or_404(queryset, pk=pk)
    #     serializer = PerformanceReviewSerializer(pr, 
    #         context={'request': request})
    #     return Response(serializer.data)

    # def update(self, request, pk=None):
    #     pr = PerformanceReview.objects.get(pk=pk)
    #     pr.evaluation_type = request.data['evaluation_type']
    #     pr.probationary_evaluation_type = \
    #         request.data['probationary_evaluation_type']
    #     pr.step_increase = request.data['step_increase']
    #     pr.top_step_bonus = request.data['top_step_bonus']
    #     pr.action_other = request.data['action_other']
    #     pr.factor_job_knowledge = request.data['factor_job_knowledge']
    #     pr.factor_work_quality = request.data['factor_work_quality']
    #     pr.factor_work_quantity = request.data['factor_work_quantity']
    #     pr.factor_work_habits = request.data['factor_work_habits']
    #     pr.factor_analysis = request.data['factor_analysis']
    #     pr.factor_initiative = request.data['factor_initiative']
    #     pr.factor_interpersonal = request.data['factor_interpersonal']
    #     pr.factor_communication = request.data['factor_communication']
    #     pr.factor_dependability = request.data['factor_dependability']
    #     pr.factor_professionalism = request.data['factor_professionalism']
    #     pr.factor_management = request.data['factor_management']
    #     pr.factor_supervision = request.data['factor_supervision']
    #     pr.evaluation_successes = request.data['evaluation_successes']
    #     pr.evaluation_opportunities = request.data['evaluation_opportunities']
    #     pr.evaluation_goals_manager = request.data['evaluation_goals_manager']
    #     pr.evaluation_comments_employee = \
    #         request.data['evaluation_comments_employee']
    #     pr.description_reviewed_employee = \
    #         request.data['description_reviewed_employee']
    #     if pr.status == PerformanceReview.NEEDS_EVALUATION and all([
    #         (pr.evaluation_type == 'A' or
    #             (pr.evaluation_type == 'P' and
    #                 pr.probationary_evaluation_type != None
    #             )
    #         ),
    #         pr.step_increase != None,
    #         pr.top_step_bonus != None,
    #         pr.factor_job_knowledge != None,
    #         pr.factor_work_quality != None,
    #         pr.factor_work_quantity != None,
    #         pr.factor_work_habits != None,
    #         pr.factor_analysis != None,
    #         pr.factor_initiative != None,
    #         pr.factor_interpersonal != None,
    #         pr.factor_communication != None,
    #         pr.factor_dependability != None,
    #         pr.factor_professionalism != None,
    #         pr.factor_management != None,
    #         pr.factor_supervision != None,
    #         len(pr.evaluation_successes) > 0,
    #         len(pr.evaluation_opportunities) > 0,
    #         len(pr.evaluation_goals_manager) > 0,
    #         pr.description_reviewed_employee
    #     ]):
    #         pr.status = PerformanceReview.EVALUATION_WRITTEN
    #         send_evaluation_written_email_to_employee(pr.employee, pr)
    #     pr.save()
    #     serialized_review = PerformanceReviewSerializer(pr,
    #         context={'request': request})
    #     return Response(serialized_review.data)
    
    def partial_update(self, request, pk=None):
        """
        Currently just updates the employee's comments. This might need to be
        more general to accept any partial updates.
        """
        tor = TimeOffRequest.objects.get(pk=pk)
        tor.acknowledged = request.data['acknowledged']
        tor.save()
        serialized_tor = TimeOffRequestSerializer(tor,
            context={'request': request})
        return Response(serialized_tor.data)

    # # TODO: Don't use this - use the ModelViewSet get
    # @action(detail=True, methods=['get'])
    # def get_a_performance_review(self, request, pk=None):
    #     review = PerformanceReview.objects.get(pk=pk)
    #     serialized_review = PerformanceReviewSerializer(review,
    #         context={'request': request})
    #     return Response(serialized_review.data)

    # A list of employees with time off requests in the same time period with]
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
