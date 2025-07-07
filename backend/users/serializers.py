from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser, ApprovedDoctor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

#I created this as a simple serializer to expose basic user info like id, username, email, and the role flags.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_doctor', 'is_patient']
# I mostly use this when I need to show who’s logged in or when sending user info to the frontend in a secure way. It’s clean and avoids unnecessary exposure of sensitive fields.


# This one handles user signup for both patients and doctors.
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    role = serializers.ChoiceField(write_only=True,choices=[("doctor", "Doctor"), ("patient", "Patient")])
    doctor_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "password", "full_name",
            "blood_type", "address", "role", "doctor_id"
        ]

    def validate(self, data):
        role = data.get("role")
        doctor_id = data.get("doctor_id")
# Instead of relying on the frontend to send is_doctor or is_patient, I added a role field.

        if role == "doctor":
            if not doctor_id:
                raise serializers.ValidationError("Doctor ID is required for doctor registration.")
            if not ApprovedDoctor.objects.filter(doctor_id=doctor_id).exists():
                raise serializers.ValidationError("Invalid Doctor ID. Contact admin if you're not pre-approved.")
# If someone tries to register as a doctor, I check if their doctor_id exists in the ApprovedDoctor table — this way, only pre-approved doctors can access doctor-specific features. That was important to ensure we’re staying HIPAA-aligned and not just letting anyone claim to be a doctor.
        return data

# In the create() method, I dynamically assign the roles and store optional data like blood_type, address, and full_name
    def create(self, validated_data):
        role = validated_data.pop("role")
        doctor_id = validated_data.pop("doctor_id", None)
# I also made sure we don’t throw errors if some optional fields are left blank which makes the UX smoother
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", ""),
            blood_type=validated_data.get("blood_type", ""),
            address=validated_data.get("address", ""),
            is_doctor=(role == "doctor"),
            is_patient=(role == "patient"),
            doctor_id=doctor_id if role == "doctor" else None
        )

        return user

# This one was necessary because as I wanted login to work with either username or email, not just username.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)        
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient
        token['is_admin'] = user.is_superuser

        return token
# I tried both paths: email first, then username. Once I find the user, I verify the password using Django’s authenticate() and then proceed further.
    def validate(self, attrs):
        login_input = attrs.get("username")
        password = attrs.get("password")

        user = CustomUser.objects.filter(email=login_input).first()
        if not user:
            user = CustomUser.objects.filter(username=login_input).first()
        if not user:
            raise AuthenticationFailed("User not found")

        authenticated_user = authenticate(username=user.username, password=password)
        if authenticated_user is None:
            raise AuthenticationFailed("Invalid credentials")
        data = super().validate({
            "username": user.username,
            "password": password
        })

        data["username"] = user.username
        data["is_admin"] = user.is_superuser
        data["is_doctor"] = user.is_doctor
        data["is_patient"] = user.is_patient
        return data


# give back id, username, and full_name, which is all I need to show in the UI when selecting a doctor or patient to chat with
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name']