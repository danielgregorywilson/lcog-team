import datetime

from django.contrib.auth.models import Group, User

from rest_framework import serializers

from people.models import (
    Employee, PerformanceReview, ReviewNote, Signature, TeleworkApplication,
    TeleworkSignature, ViewedSecurityMessage
)


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='get_full_name')
    
    class Meta:
        model = User
        fields = ['pk', 'url', 'username', 'email', 'name', 'groups', 'is_staff']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_usernames = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['pk', 'url', 'name', 'user_set', 'user_usernames']
    
    @staticmethod
    def get_user_usernames(group):
        return map(lambda user: user.username, group.user_set.all())


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(source='user.get_full_name')
    email = serializers.EmailField(source='user.email')
    is_manager = serializers.SerializerMethodField()
    has_manager = serializers.SerializerMethodField()
    is_eligible_for_telework_application = serializers.SerializerMethodField()
    is_upper_manager = serializers.SerializerMethodField()
    prs_can_view = serializers.SerializerMethodField()
    notes_can_view = serializers.SerializerMethodField()
    next_to_sign_prs = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'url', 'pk', 'name', 'user', 'email', 'manager', 'is_manager',
            'has_manager', 'is_eligible_for_telework_application',
            'is_upper_manager', 'is_hr_manager', 'is_executive_director',
            'viewed_security_message', 'prs_can_view', 'notes_can_view',
            'telework_applications_can_view', 'next_to_sign_prs'
        ]

    @staticmethod
    def get_is_manager(employee):
        return employee.get_direct_reports().count() != 0
    
    @staticmethod
    def get_has_manager(employee):
        return bool(employee.manager)

    @staticmethod
    def get_is_eligible_for_telework_application(employee):
        if not employee.manager:
            return False
        return all([ 
            not employee.is_executive_director, # Not the executive director
            not employee.manager.is_executive_director, # Not anyone who reports to the executive director (e.g. finance manager)
            employee.manager.manager and not employee.manager.manager.is_executive_director, # Not anyone who reports to the above (e.g. finance employees)
            not employee.is_division_director, # No division directors
            not employee.manager.is_division_director, # No program managers
            not employee.is_hr_manager,  # Not the HR manager
            not employee.manager.is_hr_manager  # Not anyone who reports to the HR manager
        ])

    @staticmethod
    def get_is_upper_manager(employee):
        return employee.get_direct_reports_descendants().count() != 0
    
    @staticmethod
    def get_prs_can_view(employee):
        return employee.prs_can_view()

    @staticmethod
    def get_notes_can_view(employee):
        return employee.notes_can_view()

    @staticmethod
    def get_telework_applications_can_view(employee):
        return employee.telework_applications_can_view()

    @staticmethod
    def get_next_to_sign_prs(employee):
        """
        Returns the name of the next employee who will sign the PR.
        """
        if employee.is_executive_director:
            return ""
        elif employee.is_hr_manager:
            return Employee.objects.filter(is_executive_director=True).first().user.get_full_name()
        elif employee.is_division_director:
            return Employee.objects.filter(is_hr_manager=True).first().user.get_full_name()
        elif employee.manager:
            return employee.manager.user.get_full_name()
        else:
            return ""



class PerformanceReviewSerializer(serializers.HyperlinkedModelSerializer):
    employee_pk = serializers.CharField(source='employee.pk') #TODO: Make IntegerField
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    employee_division = serializers.SerializerMethodField()
    employee_unit_or_program = serializers.SerializerMethodField()
    employee_job_title = serializers.CharField(source='employee.job_title.name')
    manager_pk = serializers.IntegerField(source='employee.manager.pk')
    manager_name = serializers.CharField(source='employee.manager.user.get_full_name')
    days_until_review = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')
    all_required_signatures = serializers.SerializerMethodField()
    position_description_link = serializers.SerializerMethodField()
    signed_position_description = serializers.FileField()
 
    class Meta:
        model = PerformanceReview
        fields = [
            'url', 'pk', 'employee_pk', 'employee_name', 'employee_division',
            'employee_unit_or_program', 'employee_job_title', 'manager_pk',
            'manager_name', 'days_until_review', 'status', 'period_start_date', 
            'period_end_date', 'effective_date', 'evaluation_type',
            'probationary_evaluation_type', 'step_increase', 'top_step_bonus',
            'action_other',

            'factor_job_knowledge', 'factor_work_quality',
            'factor_work_quantity', 'factor_work_habits', 'factor_analysis',
            'factor_initiative', 'factor_interpersonal',
            'factor_communication', 'factor_dependability',
            'factor_professionalism', 'factor_management',
            'factor_supervision', 'evaluation_successes',
            'evaluation_opportunities', 'evaluation_goals_manager',
            'evaluation_goals_employee','evaluation_comments_employee',

            'position_description_link', 'description_reviewed_employee',
            'signed_position_description', 'all_required_signatures'
        ]
    
    @staticmethod
    def get_employee_division(pr):
        if pr.employee.unit_or_program and pr.employee.unit_or_program.division:
            return pr.employee.unit_or_program.division.name
        else:
            return ''
    
    @staticmethod
    def get_employee_unit_or_program(pr):
        if pr.employee.unit_or_program:
            return pr.employee.unit_or_program.name
        else:
            return ''

    @staticmethod
    def get_days_until_review(pr):
        today = datetime.date.today()
        delta = pr.period_end_date - today
        return delta.days
    
    @staticmethod
    def get_evaluation(pr):
        if hasattr(pr, 'performanceevaluation'):
            return pr.performanceevaluation.evaluation
        else:
            return ""

    @staticmethod
    def get_position_description_link(pr):
        return pr.employee.position_description_link()

    @staticmethod
    def get_discussion_took_place(pr):
        if hasattr(pr, 'performanceevaluation'):
            return "Yes" if pr.performanceevaluation.manager_discussed else "No"
        else:
            return "No"
    
    @staticmethod
    def get_all_required_signatures(pr):
        return pr.all_required_signatures()


class PerformanceReviewFileUploadSerializer(serializers.HyperlinkedModelSerializer):
    signed_position_description = serializers.FileField()

    class Meta:
        model = PerformanceReview
        fields = [
            'url', 'signed_position_description'
        ]


class FileUploadSerializer(serializers.Serializer):
    file_upload = serializers.FileField()

    class Meta:
        fields = ['file_upload']


class SignatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Signature
        fields = [
            'url', 'pk', 'review', 'employee', 'date'
        ]


class ReviewNoteSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField()
    employee_pk = serializers.IntegerField(source='employee.pk')
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    date = serializers.DateField()
    note = serializers.CharField()
    
    class Meta:
        model = ReviewNote
        fields = ['url', 'pk', 'employee_pk', 'employee_name', 'date', 'note']


class ViewedSecurityMessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ViewedSecurityMessage
        fields = [
            'url', 'pk', 'employee', 'security_message', 'datetime'
        ]


class TeleworkApplicationSerializer(serializers.HyperlinkedModelSerializer):
    employee_name = serializers.CharField(source='employee.user.get_full_name')
    employee_pk = serializers.IntegerField(source='employee.pk')
    manager_pk = serializers.IntegerField(source='employee.manager.pk')
    manager_name = serializers.CharField(source='employee.manager.user.get_full_name')
    status = serializers.CharField(source='get_status_display')
    program_manager_signature_0 = serializers.SerializerMethodField()
    employee_signature_0 = serializers.SerializerMethodField()
    employee_signature_1 = serializers.SerializerMethodField()
    manager_signature = serializers.SerializerMethodField()
    program_manager_signature_1 = serializers.SerializerMethodField()
    division_director_signature = serializers.SerializerMethodField()
    dependent_care_documentation = serializers.FileField()
 
    class Meta:
        model = TeleworkApplication
        fields = [
            'url', 'pk', 'employee_name', 'employee_pk', 'manager_pk',
            'manager_name', 'program_manager_pk', 'program_manager_name',
            'status', 'date', 
            
            'program_manager_approve', 'hours_onsite', 'telework_location',
            'hours_working', 'duties', 'communication_when',
            'communication_time', 'communication_how',
            'equipment_provided_phone', 'equipment_provided_laptop',
            'equipment_provided_desktop', 'equipment_provided_monitor',
            'equipment_provided_access', 'equipment_provided_other',
            'equipment_provided_other_value',

            'workspace_checklist_1', 'workspace_checklist_2',
            'workspace_checklist_3', 'workspace_checklist_4',
            'workspace_checklist_5', 'workspace_checklist_6',
            'workspace_checklist_7', 'workspace_checklist_8',
            'workspace_checklist_9', 'workspace_checklist_10',
            'workspace_checklist_11', 'workspace_checklist_12',
            'emergency_checklist_1', 'emergency_checklist_2',
            'emergency_checklist_3', 'ergonomics_checklist_1',
            'ergonomics_checklist_2', 'ergonomics_checklist_3',
            'ergonomics_checklist_4', 'ergonomics_checklist_5',
            
            'teleworker_comments', 'manager_comments',
            
            'dependent_care_checklist_1', 'dependent_care_documentation',

            'program_manager_signature_0', 'employee_signature_0',
            'employee_signature_1', 'manager_signature',
            'program_manager_signature_1', 'division_director_signature'
        ]

    @staticmethod
    def get_program_manager_signature_0(application):
        return application.program_manager_signature_0()

    @staticmethod
    def get_employee_signature_0(application):
        return application.employee_signature_0()
    
    @staticmethod
    def get_employee_signature_1(application):
        return application.employee_signature_1()
    
    @staticmethod
    def get_manager_signature(application):
        return application.manager_signature()

    @staticmethod
    def get_program_manager_signature_1(application):
        return application.program_manager_signature_1()
    
    @staticmethod
    def get_division_director_signature(application):
        return application.division_director_signature()


class TeleworkApplicationFileUploadSerializer(serializers.HyperlinkedModelSerializer):
    dependent_care_documentation = serializers.FileField()

    class Meta:
        model = TeleworkApplication
        fields = [
            'url', 'dependent_care_documentation'
        ]


class TeleworkSignatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeleworkSignature
        fields = [
            'url', 'pk', 'application', 'employee', 'index', 'date'
        ]