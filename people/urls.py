from django.urls import path

from .views import PerformanceReviewEmployeeMetConfirmView, PerformanceReviewManagerMetConfirmView, PerformanceReviewView

urlpatterns = [
    path('pr/<int:pk>/', PerformanceReviewView.as_view(), name='performancereview-view'),
    path('pr/employee-met-confirm/', PerformanceReviewEmployeeMetConfirmView.as_view(), name='peformance-review-employee-met-confirm'),
    path('pr/manager-met-confirm/', PerformanceReviewManagerMetConfirmView.as_view(), name='peformance-review-manager-met-confirm')
]