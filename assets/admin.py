from django.contrib import admin
from .models import Asset, MaintenanceRecord

admin.site.register(Asset)
admin.site.register(MaintenanceRecord)
