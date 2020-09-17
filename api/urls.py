from rest_framework import routers

from django.urls import include, path

from people.api_views import EmployeeViewSet, PerformanceReviewViewSet, ReviewNoteViewSet, UserViewSet


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
]

router = routers.DefaultRouter()
router.register('v1/user', UserViewSet)
router.register('v1/employee', EmployeeViewSet)
router.register('v1/performancereview', PerformanceReviewViewSet)
router.register('v1/reviewnote', ReviewNoteViewSet)

urlpatterns = router.urls + urlpatterns
