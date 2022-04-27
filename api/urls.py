from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import include, path

from deskreservation.api_views import DeskReservationViewSet, DeskViewSet
from mainsite.api_views import TrustedIPViewSet, SecurityMessageViewSet
from mainsite.views import obtain_auth_token_without_password
from people.api_views import (
    CurrentUserView, EmployeeViewSet, FileUploadViewSet, GroupViewSet,
    PerformanceReviewViewSet, ReviewNoteViewSet, SignatureViewSet,
    TeleworkApplicationFileUploadViewSet, TeleworkApplicationViewSet,
    TeleworkSignatureViewSet, UserViewSet, ViewedSecurityMessageViewSet
)
from responsibilities.api_views import (
    ResponsibilityViewSet, TagViewSet as ResponsibilityTagViewSet
)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token_without_password),
    path('api-token-auth-password/', obtain_auth_token),
    path('v1/current-user/', CurrentUserView.as_view(), name='current_user'),
]

router = routers.DefaultRouter(trailing_slash=False)
router.register('v1/user', UserViewSet)
router.register('v1/groups', GroupViewSet)
router.register('v1/employee', EmployeeViewSet)
router.register('v1/responsibilities', ResponsibilityViewSet)
router.register('v1/responsibilitytags', ResponsibilityTagViewSet)
router.register('v1/desk', DeskViewSet)
router.register('v1/deskreservation', DeskReservationViewSet)
router.register('v1/performancereview', PerformanceReviewViewSet)
router.register('v1/fileupload', FileUploadViewSet, basename='fileupload')
router.register('v1/telework-fileupload', TeleworkApplicationFileUploadViewSet, basename='telework-fileupload')
router.register('v1/signature', SignatureViewSet)
router.register('v1/reviewnote', ReviewNoteViewSet)
router.register('v1/securitymessage', SecurityMessageViewSet)
router.register('v1/viewedsecuritymessage', ViewedSecurityMessageViewSet)
router.register('v1/teleworkapplication', TeleworkApplicationViewSet)
router.register('v1/teleworksignature', TeleworkSignatureViewSet)
router.register('v1/trustedip', TrustedIPViewSet, basename='trustedip')

urlpatterns = router.urls + urlpatterns
