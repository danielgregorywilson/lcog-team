from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User

from mainsite.helpers import get_host_url, is_true_string, send_evaluation_complete_email

from people.models import Employee, PerformanceReview, ReviewNote
from people.serializers import EmployeeSerializer, PerformanceReviewSerializer, ReviewNoteSerializer, UserSerializer


class CurrentUserView(RetrieveAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get_object(self):
        return getattr(self.request.user, 'employee', None)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Return a list of all employees. Optionally filter by direct reports
        """
        queryset = Employee.objects.all() # Default queryset

        # Optionally filter by direct reports
        user = self.request.user
        direct_reports = self.request.query_params.get('direct-reports', None)
        if direct_reports is not None and direct_reports == "True":
            queryset = Employee.objects.filter(manager__user=user)
        return queryset
    
    @action(detail=True, methods=['get'])
    def employee_next_performance_review(self, request, pk=None):
        next_review = request.user.employee.employee_next_review()
        serialized_review = PerformanceReviewSerializer(next_review, context={'request': request})
        return Response(serialized_review.data)


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """

    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.AllowAny] # TODO

    def get_queryset(self):
        """
        This view should return a list of all performance reviews for which
        the currently authenticated user is the manager.
        """
        user = self.request.user
        if user.is_authenticated:
            queryset = PerformanceReview.objects.filter(employee__manager__user=user) # Default queryset
            upper_manager = self.request.query_params.get('upper_manager', None)
            action_required = self.request.query_params.get('action_required', None)
            if is_true_string(upper_manager):
                if action_required is not None:
                    if is_true_string(action_required):
                        queryset = PerformanceReview.upper_manager_upcoming_reviews_action_required.get_queryset(user)
                    else:
                        queryset = PerformanceReview.upper_manager_upcoming_reviews_no_action_required.get_queryset(user)    
                else:
                    queryset = PerformanceReview.upper_manager_all_relevant_upcoming_reviews.get_queryset(user)
            elif action_required is not None:
                if is_true_string(action_required):
                    queryset = PerformanceReview.manager_upcoming_reviews_action_required.get_queryset(user)
                else:
                    queryset = PerformanceReview.manager_upcoming_reviews_no_action_required.get_queryset(user)
            else:
                queryset = PerformanceReview.manager_upcoming_reviews.get_queryset(user)
        else:
            queryset = PerformanceReview.objects.all()
        return queryset

    def update(self, request, pk=None):
        pr = PerformanceReview.objects.get(pk=pk)
        pr.evaluation_successes = request.data['evaluationSuccesses']
        pr.evaluation_opportunities = request.data['evaluationOpportunities']
        pr.evaluation_goals_manager = request.data['evaluationGoalsManager']
        pr.evaluation_comments_employee = request.data['evaluationCommentsEmployee']
        if pr.status == PerformanceReview.NEEDS_EVALUATION and pr.evaluation_successes:
            pr.status = PerformanceReview.EVALUATION_WRITTEN
        pr.save()
        serialized_review = PerformanceReviewSerializer(pr, context={'request': request})
        return Response(serialized_review.data)

    # TODO: Don't use this - use the ModelViewSet get
    @action(detail=True, methods=['get'])
    def get_a_performance_review(self, request, pk=None):
        review = PerformanceReview.objects.get(pk=pk)
        serialized_review = PerformanceReviewSerializer(review, context={'request': request})
        return Response(serialized_review.data)

    @action(detail=True, methods=['put'])
    def manager_mark_discussed(self, request, pk=None):
        review = self.get_object()
        evaluation = review.performanceevaluation
        evaluation.manager_discussed = True
        evaluation.save()
        if evaluation.employee_discussed:
            review.status = PerformanceReview.EVALUATION_COMPLETED
            review.save()
            send_evaluation_complete_email([review.employee.manager.manager.user.email], review, get_host_url(self.request))
        return Response({'status': 'performance review marked as discussed by manager'})
    
    @action(detail=True, methods=['put'])
    def employee_mark_discussed(self, request, pk=None):
        review = PerformanceReview.objects.get(pk=pk)
        evaluation = review.performanceevaluation
        evaluation.employee_discussed = True
        evaluation.save()
        if evaluation.manager_discussed:
            review.status = PerformanceReview.EVALUATION_COMPLETED
            review.save()
            send_evaluation_complete_email([review.employee.manager.manager.user.email], review, get_host_url(self.request))
        return Response({'status': 'performance review marked as discussed by employee'})


class ReviewNoteViewSet(viewsets.ModelViewSet):
    queryset = ReviewNote.objects.all()
    serializer_class = ReviewNoteSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.AllowAny] # TODO

    def get_queryset(self):
        """
        This view should return a list of all review notes written by this user.
        """
        user = self.request.user
        # TODO: Don't do this. There is an issue where the detail view doesn't have the user
        if user.is_anonymous:
            return ReviewNote.objects.all()
        else:
            return ReviewNote.objects.filter(manager__user=user)

    def create(self, request):
        employee = Employee.objects.get(pk=request.data['employee_pk'])
        manager = employee.manager
        note = request.data['note']
        new_review_note = ReviewNote.objects.create(manager=manager, employee=employee, note=note)
        serialized_note = ReviewNoteSerializer(new_review_note, context={'request': request})
        return Response(serialized_note.data)
    
    def update(self, request, pk=None):
        employee = Employee.objects.get(pk=request.data['employee_pk'])
        review_note = ReviewNote.objects.get(pk=pk)
        review_note.employeee = employee
        review_note.note = request.data['note']
        review_note.save()
        serialized_note = ReviewNoteSerializer(review_note, context={'request': request})
        return Response(serialized_note.data)
      
    # TODO: Detail false?
    @action(detail=True, methods=['get'])
    def notes_for_employee(self, request, pk=None):
        review_notes = ReviewNote.objects.filter(manager=request.user.employee.pk, employee=pk)
        serialized_notes = [ReviewNoteSerializer(note, context={'request': request}).data for note in review_notes]
        return Response(serialized_notes)