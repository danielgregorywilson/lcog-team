from django.contrib.auth.models import User
from django.http.response import HttpResponse

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

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


def health_check_view(request):
    return HttpResponse("OK")