from django.urls import path
from .views import AssetListCreateView, MaintenanceRecordListCreateView

urlpatterns = [
    path('assets/', AssetListCreateView.as_view(), name='asset-list-create'),
    path('maintenance-records/', MaintenanceRecordListCreateView.as_view(), name='maintenance-record-list-create'),
]
