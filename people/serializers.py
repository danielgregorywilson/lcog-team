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
    class Meta:
        model = Employee
        fields = ['user', 'manager', 'hire_date', 'salary',]


class PerformanceReviewSerializer(serializers.HyperlinkedModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    date_of_review = serializers.DateField(source='date')
    days_until_review = serializers.SerializerMethodField()
    status = serializers.CharField()
    date_of_discussion = serializers.DateField(source='performanceevaluation.discussion_date')
    discussion_took_place = serializers.SerializerMethodField()
    
    class Meta:
        model = PerformanceReview
        fields = ['employee_name', 'date_of_review', 'days_until_review', 'status', 'date_of_discussion', 'discussion_took_place',]
    
    @staticmethod
    def get_days_until_review(pr):
        out = None
        return 1

        if assignment and assignment.status == Assignment.STATUS_DONE:
            take = assignment.latest_submitted_take()
            if take:
                out = {
                    'correct': int(take.score),
                    'possible': int(take.total_score),
                    'teacherViewResultsUrl': "{0}?takeId={1}".format(reverse('assessment_quiz_results_teacher', kwargs={'pk': assignment.id}), take.id),
                    'studentViewResultsUrl': "{0}?takeId={1}".format(reverse('assessment_quiz_results_student', kwargs={'pk': assignment.id}), take.id)
                }
        return out
    
    @staticmethod
    def get_discussion_took_place(pr):
        out = None
        return "Yes"

        if assignment and assignment.status == Assignment.STATUS_DONE:
            take = assignment.latest_submitted_take()
            if take:
                out = {
                    'correct': int(take.score),
                    'possible': int(take.total_score),
                    'teacherViewResultsUrl': "{0}?takeId={1}".format(reverse('assessment_quiz_results_teacher', kwargs={'pk': assignment.id}), take.id),
                    'studentViewResultsUrl': "{0}?takeId={1}".format(reverse('assessment_quiz_results_student', kwargs={'pk': assignment.id}), take.id)
                }
        return out


class ReviewNoteSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField()
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    date = serializers.DateField()
    note = serializers.CharField()
    
    class Meta:
        model = ReviewNote
        fields = ['pk', 'employee_name', 'date', 'note']