from rest_framework import routers

from django.urls import include, path

from people.api_views import CurrentUserView, EmployeeViewSet, PerformanceReviewViewSet, ReviewNoteViewSet, UserViewSet


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('v1/current-user/', CurrentUserView.as_view(), name='current_user'),
]

router = routers.DefaultRouter()
# router.register('v1/current-user', CurrentUserView)
router.register('v1/user', UserViewSet)
router.register('v1/employee', EmployeeViewSet)
router.register('v1/performancereview', PerformanceReviewViewSet)
router.register('v1/reviewnote', ReviewNoteViewSet)

urlpatterns = router.urls + urlpatterns
