from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, RegistrationSerializer, MaintenanceRecordSerializer, AssetSerializer
from .models import MaintenanceRecord, Asset
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import LoginSerializer



CustomUser = get_user_model()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


class MaintenanceRecordListCreateView(generics.ListCreateAPIView):
    queryset = MaintenanceRecord.objects.all()
    serializer_class = MaintenanceRecordSerializer


class AssetListCreateView(generics.ListCreateAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer


class CustomUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=RegistrationSerializer,
        responses={status.HTTP_201_CREATED: RegistrationSerializer()},
        operation_summary="Register a new user",
        operation_description="Creates a new user account.",
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: 'Successful login. Returns a token.',
            400: 'Invalid input. Missing or incorrect parameters.',
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)
