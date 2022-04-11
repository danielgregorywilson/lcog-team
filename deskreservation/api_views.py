from datetime import datetime

from django.utils.timezone import get_current_timezone

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Desk, DeskReservation
from .serializers import DeskReservationSerializer, DeskSerializer
from people.models import Employee


class DeskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for desk reservations.
    """
    queryset = Desk.objects.all()
    serializer_class = DeskSerializer

    # def get_queryset(self):
    #     """
    #     Return a list of all responsibilities to any authenticated user.
    #     Optionally filter by orphaned responsibilities.
    #     Optionally filter by employee pk to get primary responsibilities with
    #     secondaries, or just a list of secondaries.
    #     """
    #     import pdb; pdb.set_trace();
    #     user = self.request.user
    #     if user.is_authenticated:
    #         orphaned = self.request.query_params.get('orphaned', None)
    #         if orphaned is not None and orphaned == "true":
    #             queryset = Responsibility.objects.filter(
    #                 Q(primary_employee__isnull=True) | Q(secondary_employee__isnull=True)
    #             )
    #         employee = self.request.query_params.get('employee', None)
    #         if employee is not None and employee.isdigit():
    #             secondary = self.request.query_params.get('secondary', None)
    #             if secondary is not None and secondary == 'true':
    #                 queryset = Responsibility.objects.filter(secondary_employee=employee)
    #             else:
    #                 queryset = Responsibility.objects.filter(primary_employee=employee)
    #     else:
    #         queryset = Responsibility.objects.none()
    #     return queryset if 'queryset' in locals() else Responsibility.objects.all()


class DeskReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for desk reservations.
    """
    queryset = DeskReservation.currently_reserved_objects.all()
    serializer_class = DeskReservationSerializer

    def create(self, request):
        employee = Employee.objects.get(pk=request.data['employee_pk']) if request.data['employee_pk'] != -1 else None
        desk = Desk.objects.get(number=request.data['desk_number']) if request.data['desk_number'] != -1 else None
        existing_reservations = DeskReservation.objects.filter(desk=desk, check_out__isnull=True)
        if existing_reservations.count():
            serialized_reservation = DeskReservationSerializer(existing_reservations[0],
                context={'request': request})
            return Response({**serialized_reservation.data, 'created': False})
        else:
            reservation = DeskReservation.objects.create(employee=employee, desk=desk)
            serialized_reservation = DeskReservationSerializer(reservation,
                context={'request': request})
            return Response({**serialized_reservation.data, 'created': True})

    @action(detail=True, methods=['put'], url_path='cancel-reservation', url_name='cancel-reservation')
    def cancel_reservation(self, request, pk=None):
        reservation = DeskReservation.objects.get(pk=pk)
        reservation.check_out = datetime.now(tz=get_current_timezone())
        reservation.save()
        serialized_reservation = DeskReservationSerializer(reservation,
            context={'request': request})
        return Response(serialized_reservation.data)