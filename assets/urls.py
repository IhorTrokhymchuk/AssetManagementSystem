# assets/urls.py
from django.urls import path
from .views import AssetListCreateView, MaintenanceRecordListCreateView, UserDetailsView, CustomUserListView, RegistrationView, LoginView

urlpatterns = [
    path('assets/', AssetListCreateView.as_view(), name='asset-list-create'),
    path('maintenance-records/', MaintenanceRecordListCreateView.as_view(), name='maintenance-record-list-create'),
    path('users/', CustomUserListView.as_view(), name='customuser-list'),
    path('user-details/<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # add other paths as needed
]
