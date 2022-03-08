from rest_framework import viewsets
from rest_framework.response import Response

from django.db.models import Q

from people.models import Employee

from .models import Responsibility
from .serializers import ResponsibilitySerializer


class ResponsibilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Responsibility.objects.all()
    serializer_class = ResponsibilitySerializer

    def get_queryset(self):
        """
        Return a list of all responsibilities to any authenticated user.
        Optionally filter by orphaned responsibilities.
        Optionally filter by employee pk to get primary responsibilities with
        secondaries, or just a list of secondaries.
        """
        user = self.request.user
        if user.is_authenticated:
            orphaned = self.request.query_params.get('orphaned', None)
            if orphaned is not None and orphaned == "true":
                queryset = Responsibility.objects.filter(
                    Q(primary_employee__isnull=True) | Q(secondary_employee__isnull=True)
                )
            employee = self.request.query_params.get('employee', None)
            if employee is not None and employee.isdigit():
                secondary = self.request.query_params.get('secondary', None)
                if secondary is not None and secondary == 'true':
                    queryset = Responsibility.objects.filter(secondary_employee=employee)
                else:
                    queryset = Responsibility.objects.filter(primary_employee=employee)
        else:
            queryset = Responsibility.objects.none()
        return queryset if 'queryset' in locals() else Responsibility.objects.all()

    def create(self, request):
        name = request.data['name']
        link = request.data['link'] if 'link' in request.data else ''
        primary_employee = Employee.objects.get(pk=request.data['primary_employee']) if request.data['primary_employee'] != -1 else None
        secondary_employee = Employee.objects.get(pk=request.data['secondary_employee']) if request.data['secondary_employee'] != -1 else None
        responsibility = Responsibility.objects.create(name=name, link=link, primary_employee=primary_employee, secondary_employee=secondary_employee)
        serialized_responsibility = ResponsibilitySerializer(responsibility,
            context={'request': request})
        return Response(serialized_responsibility.data)

    def update(self, request, pk=None):
        responsibility = Responsibility.objects.get(pk=pk)
        name = request.data['name']
        link = request.data['link'] if 'link' in request.data else ''
        primary_employee = Employee.objects.get(pk=request.data['primary_employee']) if request.data['primary_employee'] != -1 else None
        secondary_employee = Employee.objects.get(pk=request.data['secondary_employee']) if request.data['secondary_employee'] != -1 else None
        responsibility.name = name
        responsibility.link = link
        responsibility.primary_employee = primary_employee
        responsibility.secondary_employee = secondary_employee
        responsibility.save()
        serialized_responsibility = ResponsibilitySerializer(responsibility,
            context={'request': request})
        return Response(serialized_responsibility.data)
