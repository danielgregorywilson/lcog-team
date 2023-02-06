from rest_framework import serializers

from workflows.models import (
    Action, EmployeeTransition, Process, ProcessInstance, Role, Step,
    StepChoice, StepInstance, Workflow, WorkflowInstance
)


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ['url', 'pk', 'name', 'description', 'members']


class StepChoiceSerializer(serializers.HyperlinkedModelSerializer):
    next_step_pk = serializers.IntegerField(source="next_step.pk")
    
    class Meta:
        model = StepChoice
        fields = '__all__'
        fields = [
            'pk', 'order', 'choice_text', 'step', 'next_step', 'next_step_pk'
        ]


class ActionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class StepSerializer(serializers.HyperlinkedModelSerializer):
    next_step_choices = StepChoiceSerializer(many=True)
    role = RoleSerializer()
    process_role_pk = serializers.SerializerMethodField()
    workflow_role_pk = serializers.SerializerMethodField()
    completion_action = ActionSerializer()
    optional_actions = ActionSerializer(many=True)
    
    class Meta:
        model = Step
        fields = [
            'url', 'pk', 'order', 'start', 'end', 'name', 'description',
            'choices_prompt', 'role', 'next_step', 'next_step_choices',
            'process_role_pk', 'workflow_role_pk', 'completion_action',
            'optional_actions'
        ]
    
    @staticmethod
    def get_process_role_pk(step):
        return step.process.role.pk if step.process.role else None
    
    @staticmethod
    def get_workflow_role_pk(step):
        return step.process.workflow.role.pk if step.process.workflow.role else None


class ProcessSerializer(serializers.ModelSerializer):
    steps = StepSerializer(source='step_set', many=True)
    
    class Meta:
        model = Process
        fields = [
            'url', 'pk', 'name', 'version', 'steps'
        ]


class WorkflowSerializer(serializers.HyperlinkedModelSerializer):
    processes = ProcessSerializer(many=True)

    class Meta:
        model = Workflow
        fields = [
            'url', 'pk', 'name', 'version', 'processes'
        ]


class StepInstanceSerializer(serializers.ModelSerializer):
    step = StepSerializer(required=False)
    completed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StepInstance
        fields = [
            'url', 'pk', 'started_at', 'completed_at', 'step', 'completed_by',
            'completed_by_name'
        ]
    
    @staticmethod
    def get_completed_by_name(stepinstance):
        if stepinstance.completed_by:
            return stepinstance.completed_by.name
        else:
            return None


class ProcessInstanceSerializer(serializers.ModelSerializer):
    step_instances = StepInstanceSerializer(source='stepinstance_set',
        many=True)
    current_step_instance = StepInstanceSerializer()

    class Meta:
        model = ProcessInstance
        fields = [
            'url', 'pk', 'process', 'step_instances', 'current_step_instance',
            'completed_at'
        ]
        depth = 1


class EmployeeTransitionSerializer(serializers.ModelSerializer):
    # process_instances = ProcessInstanceSerializer(source='processinstance_set',
    #     many=True)
    # percent_complete = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeTransition
        # fields = '__all__'
        fields = [
            'url', 'pk', 'type'
        ]


class WorkflowInstanceSerializer(serializers.ModelSerializer):
    process_instances = ProcessInstanceSerializer(source='processinstance_set',
        many=True)
    percent_complete = serializers.SerializerMethodField()
    transition = EmployeeTransitionSerializer()

    class Meta:
        model = WorkflowInstance
        fields = [
            'url', 'pk', 'workflow', 'started_at', 'completed_at',
            'process_instances', 'percent_complete', 'transition'
        ]
        depth = 1

    @staticmethod
    def get_percent_complete(wfi):
        return wfi.percent_complete
