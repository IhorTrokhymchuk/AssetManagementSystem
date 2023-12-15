from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Asset, MaintenanceRecord
from django.contrib.auth import authenticate

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

    id = serializers.IntegerField(help_text='ID користувача')
    username = serializers.CharField(help_text='Ім\'я користувача')
    email = serializers.EmailField(help_text='Email користувача')
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLES, help_text='Роль користувача')


class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    maintenance_history = MaintenanceRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'

    def validate_owner(self, value):
        if not value.isalpha():
            raise serializers.ValidationError('Owner name should contain only alphabetical characters.')
        return value

    def validate(self, data):
        existing_assets = Asset.objects.filter(name=data['name'], location=data['location'])
        if existing_assets.exists():
            raise serializers.ValidationError('An asset with the same name and location already exists.')
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError('Both username and password are required.')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid username or password.')

        # Add the authenticated user to the data dictionary
        data['user'] = user

        return data