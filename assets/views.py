from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Asset, MaintenanceRecord
from .serializers import AssetSerializer, MaintenanceRecordSerializer


class AssetListCreateView(APIView):
    def get(self, request):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaintenanceRecordListCreateView(APIView):
    def get(self, request):
        maintenance_records = MaintenanceRecord.objects.all()
        serializer = MaintenanceRecordSerializer(maintenance_records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaintenanceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
