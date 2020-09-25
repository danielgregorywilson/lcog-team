import datetime

from django.contrib.auth.models import User

from rest_framework import serializers

from people.models import Employee, PerformanceReview, ReviewNote


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='get_full_name')
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'name', 'groups', 'is_staff',]


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    employee_name = serializers.CharField(source='user.get_full_name')
    
    class Meta:
        model = Employee
        fields = ['url', 'pk', 'employee_name', 'user', 'manager', 'hire_date', 'salary',]


class PerformanceReviewSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField()
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    date_of_review = serializers.DateField(source='date')
    days_until_review = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    date_of_discussion = serializers.DateField(source='performanceevaluation.discussion_date')
    evaluation = serializers.SerializerMethodField()
    discussion_took_place = serializers.SerializerMethodField()
    
    class Meta:
        model = PerformanceReview
        fields = ['url', 'pk', 'employee_name', 'date_of_review', 'days_until_review', 'status', 'date_of_discussion', 'evaluation', 'discussion_took_place',]
    
    @staticmethod
    def get_days_until_review(pr):
        today = datetime.date.today()
        delta = pr.date - today
        return delta.days
    
    @staticmethod
    def get_evaluation(pr):
        if hasattr(pr, 'performanceevaluation'):
            return pr.performanceevaluation.evaluation
        else:
            return ""

    @staticmethod
    def get_discussion_took_place(pr):
        if hasattr(pr, 'performanceevaluation'):
            return "Yes" if pr.performanceevaluation.manager_discussed else "No"
        else:
            return "No"


class ReviewNoteSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField()
    employee_pk = serializers.IntegerField(source='employee.pk')
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    date = serializers.DateField()
    note = serializers.CharField()
    
    class Meta:
        model = ReviewNote
        fields = ['url', 'pk', 'employee_pk', 'employee_name', 'date', 'note']