import json
import traceback

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from mainsite.helpers import record_error
from mainsite.models import SecurityMessage, TrustedIPAddress
from mainsite.serializers import (
    FileUploadSerializer, SecurityMessageSerializer,
    TrustedIPSerializer
)
from purchases.models import Expense

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'

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


class LogErrorView(viewsets.ViewSet):

    def create(self, request):
        record_error(
            json.dumps(request.data), None, request, traceback.format_exc()
        )
        return Response("Client error recorded", status=202)


class TrustedIPViewSet(viewsets.ViewSet):
    """
    Viewset listing trusted IP addresses
    """

    serializer_class = TrustedIPSerializer

    def list(self, request):
        admin_ips = map(lambda ip: ip.address, TrustedIPAddress.objects.all())
        settings_ips = settings.REST_FRAMEWORK_TRUSTED_IPS_LIST
        trusted_ips = list(admin_ips) + settings_ips
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = request.META.get('REMOTE_ADDR')
        return Response(client_ip in trusted_ips)


class FileUploadViewSet(viewsets.ViewSet):
    serializer_class = FileUploadSerializer
    # permission_classes = [IsAuthenticated]

    # def list(self, request):
    #     queryset = PerformanceReview.objects.all()
    #     serializer = PerformanceReviewFileUploadSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     queryset = PerformanceReview.objects.all()
    #     pr = get_object_or_404(queryset, pk=pk)
    #     serializer = PerformanceReviewFileUploadSerializer(pr, context={'request': request})
    #     return Response(serializer.data)
    
    def create(self, request):
        file_upload = request.FILES.get('file')
        if not file_upload:
            return Response(data="Missing file", status=400)
        app_label = request.data.get('content_type_app_label')
        model = request.data.get('content_type_model')
        if not app_label or not model:
            return Response(data="Missing content type", status=400)
        # TODO: Trying to generalize this with content_type in case we want to
        # use this for generic models, but maybe this is not necessary as there
        # will always be custom requirements.
        # content_type = ContentType.objects.get(app_label=app_label, model=model)
        object_pk = request.data.get('object_pk')
        if model == 'expense':
            if not object_pk:
                expense = Expense.objects.create(receipt=file_upload)
            else:
                # TODO: Object_pk should probably be an integer, but it's a string
                expense = Expense.objects.filter(pk=object_pk)
                expense.save()
            return Response(
                data=request.build_absolute_uri(expense.receipt.url),
                status=200
            )


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