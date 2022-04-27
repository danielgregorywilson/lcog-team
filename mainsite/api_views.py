from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings
from django.shortcuts import get_object_or_404

from mainsite.models import SecurityMessage, TrustedIPAddress
from mainsite.serializers import TrustedIPSerializer, SecurityMessageSerializer


# class EitherAuthenticatedOrOnSafelistPermission(permissions.BasePermission):
#     """
#     Ensure the request's IP address is on the safe list configured in Django
#     settings.
#     """

#     def has_permission(self, request, view):
#         is_authenticated = request.user.is_authenticated
#         if is_authenticated:
#             return True
        
#         remote_addr = request.META['REMOTE_ADDR']

#         # Allow if address is in the list of safe IPs in Django settings
#         for valid_ip in settings.REST_FRAMEWORK_TRUSTED_IPS_LIST:
#             if remote_addr == valid_ip or remote_addr.startswith(valid_ip):
#                 return True
#         # Allow if address is in the list of safe IPs in Django backend
#         for valid_ip in TrustedIPAddress.objects.all():
#             if remote_addr == valid_ip:
#                 return True
        
#         return False


class TrustedIPViewSet(viewsets.ViewSet):
    """
    Viewset listing trusted IP addresses
    """

    serializer_class = TrustedIPSerializer

    def list(self, request):
        admin_ips = map(lambda ip: ip.address, TrustedIPAddress.objects.all())
        settings_ips = settings.REST_FRAMEWORK_TRUSTED_IPS_LIST
        trusted_ips = list(admin_ips) + settings_ips
        client_ip = request.META['REMOTE_ADDR']
        return Response(client_ip in trusted_ips)


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