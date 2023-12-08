import base64
import os
import requests
import traceback

from django.contrib.auth.models import User
from django.http.response import HttpResponse

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from mainsite.helpers import record_error
from mainsite.serializers import AuthTokenSerializerWithoutPassword
from people.models import Employee


class ObtainAuthTokenWithoutPassword(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializerWithoutPassword
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
        except User.DoesNotExist:
            user = User.objects.create(username=serializer.initial_data['username'].split('@')[0], first_name=serializer.initial_data['firstName'], last_name=serializer.initial_data['lastName'], email=serializer.initial_data['username'])
            Employee.objects.create(user=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token_without_password = ObtainAuthTokenWithoutPassword.as_view()

class ObtainZoomAccessToken(APIView):
    def post(self, request, *args, **kwargs):
        client_id = os.environ.get('ZOOM_CLIENT_ID')
        client_secret = os.environ.get('ZOOM_CLIENT_SECRET')
        redirect_url = os.environ.get('ZOOM_REDIRECT_URL')
        ascii_string = f'{ client_id }: { client_secret }'.encode('ascii')
        encoded_string = base64.b64encode(ascii_string).decode('ascii')
        encoded_string = 'UEZ2akZ4UUVSbXFlTUtsYUpfUjRnOmUwTkZ4YzRzV3lVdnZIWHdvS0hzQW04QjJvb0JXMnBD'
        try:
            response = requests.post(
                'https://zoom.us/oauth/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': request.data['code'],
                    'redirect_uri': redirect_url,
                },
                headers={
                    'Authorization': f'Basic { encoded_string }',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            )
            return Response(response)
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            record_error(
                'Request exception:', e, request, traceback.format_exc()
            )

obtain_zoom_access_token = ObtainZoomAccessToken.as_view()


class CreateNewZoomMeeting(APIView):
    def post(self, request, *args, **kwargs):
        userId = request.data['userId']
        accessToken = request.data['accessToken']
        try:
            response = requests.post(
                f'https://api.zoom.us/v2/users/{ userId }/meetings',
                data={
                    "agenda": "Test Meeting"
                },
                headers={
                    'Authorization': f'Bearer { accessToken }',
                    'Content-Type': 'multipart/form-data'
                }
            )
            record_error(
                'Here is the response', response, request, traceback.format_exc()
            )
            return Response(response)
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            record_error(
                'Request exception:', e, request, traceback.format_exc()
            )

create_new_zoom_meeting = CreateNewZoomMeeting.as_view()


def health_check_view(request):
    return HttpResponse("OK")