from rest_framework import permissions, viewsets

from django.contrib.auth.models import User

from people.models import Employee, PerformanceReview, ReviewNote
from people.serializers import EmployeeSerializer, PerformanceReviewSerializer, ReviewNoteSerializer, UserSerializer


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

    def get_queryset(self):
        """
        This view should return a list of all review notes written by this user.
        """
        user = self.request.user
        return ReviewNote.objects.filter(manager__user=user)