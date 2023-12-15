from django.contrib.auth.models import User
from .models import Asset, MaintenanceRecord
from .serializers import AssetSerializer, MaintenanceRecordSerializer, RegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema


class AssetListCreateView(APIView):
    def get(self, request):
        assets = Asset.objects.all()
        serializer = AssetSerializer(assets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AssetSerializer)
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

    @swagger_auto_schema(request_body=AssetSerializer)
    def post(self, request):
        serializer = MaintenanceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationView(APIView):
    permission_classes = []

    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return Response({'error': 'Username or email already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        token = Token.objects.create(user=user)

        serializer = RegistrationSerializer(user)
        return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
