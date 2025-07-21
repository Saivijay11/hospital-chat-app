from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser, ApprovedDoctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    doctor_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "password", "full_name",
            "blood_type", "address", "doctor_id"
        ]

    def validate_doctor_id(self, doctor_id):
        """
        If a user provides a doctor_id, verify it exists in the ApprovedDoctor list.
        """
        if doctor_id and not ApprovedDoctor.objects.filter(doctor_id=doctor_id).exists():
            raise serializers.ValidationError("Invalid Doctor ID. Contact admin for approval.")
        return doctor_id

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['is_admin'] = user.is_superuser
        token['doctor_id'] = user.doctor_id
        return token

    def validate(self, attrs):
        login_input = attrs.get("username")
        password = attrs.get("password")

        # Try login using email or username
        user = CustomUser.objects.filter(email=login_input).first() or \
               CustomUser.objects.filter(username=login_input).first()

        if not user:
            raise AuthenticationFailed("User not found")

        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is None:
            raise AuthenticationFailed("Invalid credentials")

        # Generate token
        data = super().validate({
            "username": user.username,
            "password": password
        })

        # Extra data for frontend
        data["user_id"] = user.id
        data["username"] = user.username
        data["email"] = user.email
        data["full_name"] = user.full_name
        data["doctor_id"] = user.doctor_id
        data["is_admin"] = user.is_superuser

        return data

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name']
