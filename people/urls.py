from django.urls import path

from .views import (
    PerformanceReviewApprovalView, PerformanceReviewEmployeeMetConfirmView,
    PerformanceReviewManagerMetConfirmView, PerformanceReviewView,
    ReviewNoteCreateView, ReviewNoteDeleteView, ReviewNoteUpdateView
)

urlpatterns = [
    ###########################
    ### Performance Reviews ###
    ###########################

    # Employee
    path('pr/employee-met-confirm/',
        PerformanceReviewEmployeeMetConfirmView.as_view(),
        name='peformance-review-employee-met-confirm'),
    
    # Manager
    path('pr/<int:pk>/', PerformanceReviewView.as_view(),
        name='performancereview-view'),
    path('pr/manager-met-confirm/',
        PerformanceReviewManagerMetConfirmView.as_view(),
        name='peformance-review-manager-met-confirm'),
    # Review Notes
    path('note/add/', ReviewNoteCreateView.as_view(), name='note-create'),
    path('note/<int:pk>/', ReviewNoteUpdateView.as_view(), name='note-update'),
    path('note/<int:pk>/delete/', ReviewNoteDeleteView.as_view(),
        name='note-delete'),
    
    # Upper Manager
    path('pr/approve/<int:pk>/', PerformanceReviewApprovalView.as_view(),
        name='performancereview-approval-view'),
]