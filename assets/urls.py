from django.urls import path
from .views import AssetListCreateView, MaintenanceRecordListCreateView, LoginView, RegistrationView

urlpatterns = [
    path('assets/', AssetListCreateView.as_view(), name='asset-list-create'),
    path('maintenance-records/', MaintenanceRecordListCreateView.as_view(), name='maintenance-record-list-create'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/registration/', RegistrationView.as_view(), name='auth-registration'),
]
