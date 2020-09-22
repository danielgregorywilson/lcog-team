from rest_framework import permissions, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.models import User

from people.models import Employee, PerformanceReview, ReviewNote
from people.serializers import EmployeeSerializer, PerformanceReviewSerializer, ReviewNoteSerializer, UserSerializer


class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


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


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """

    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     self.request.user.accounts.all()
    #     return PerformanceReview.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all performance reviews for which
        the currently authenticated user is the manager.
        """
        user = self.request.user
        queryset = PerformanceReview.objects.filter(employee__manager__user=user) # Default queryset
        # TODO: Should be able to filter by upper/manager upcoming PRs which require/don't require action
        action_required = self.request.query_params.get('action_required', None)
        if action_required is not None:
            if action_required == "True":
                queryset = PerformanceReview.manager_upcoming_reviews_action_required.get_queryset(user)
            elif action_required == "False":
                queryset = PerformanceReview.manager_upcoming_reviews_no_action_required.get_queryset(user)
        return queryset


class ReviewNoteViewSet(viewsets.ModelViewSet):
    queryset = ReviewNote.objects.all()
    serializer_class = ReviewNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all review notes written by this user.
        """
        user = self.request.user
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
        note = request.data['note']
        review_note = ReviewNote.objects.get(pk=pk)
        review_note.employeee = employee
        review_note.note = note
        review_note.save()
        serialized_note = ReviewNoteSerializer(review_note, context={'request': request})
        return Response(serialized_note.data)