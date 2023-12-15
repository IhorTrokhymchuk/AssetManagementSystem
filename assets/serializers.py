from rest_framework import serializers
from .models import Asset, MaintenanceRecord


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    maintenance_history = MaintenanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'
