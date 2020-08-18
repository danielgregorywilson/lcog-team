from django.contrib.auth.models import User
from rest_framework import permissions, serializers, viewsets
from people.models import Employee, PerformanceReview


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'is_staff',]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'manager', 'hire_date', 'salary',]


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PerformanceReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['employee', 'date', 'status',]


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing the accounts
    associated with the user.
    """
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_queryset(self):
    #     self.request.user.accounts.all()
    #     return PerformanceReview.objects.all()