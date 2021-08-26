from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from mainsite.models import SecurityMessage
from mainsite.serializers import SecurityMessageSerializer


class SecurityMessageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing the current Security Message.
    """

    queryset = SecurityMessage.objects.all()
    serializer_class = SecurityMessageSerializer

    def retrieve(self, request, pk=None):
        queryset = SecurityMessage.objects.all()
        security_message = get_object_or_404(queryset, pk=pk)
        serializer = SecurityMessageSerializer(security_message, 
            context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def get_latest_security_message(self, request):
        security_message = SecurityMessage.objects.filter(active=True).latest()
        serialized_message = SecurityMessageSerializer(security_message,
            context={'request': request})
        return Response(serialized_message.data)