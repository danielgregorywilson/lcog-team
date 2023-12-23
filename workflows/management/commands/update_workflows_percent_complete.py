from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from workflows.models import ProcessInstance, WorkflowInstance


class Command(BaseCommand):
    help = 'Updates percent_complete for all ProcessInstances and WorkflowInstances'

    def handle(self, *args, **options):
        for pi in ProcessInstance.objects.all():
            pi.update_percent_complete()
            pi.save()
        for wi in WorkflowInstance.objects.all():
            wi.update_percent_complete()
            wi.save()