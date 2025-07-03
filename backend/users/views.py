from rest_framework import generics, permissions
from users.models import CustomUser
from users.serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import PublicUserSerializer
from users.serializers import UserSerializer 


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]



class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "user_id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "is_doctor": user.is_doctor,
            "is_patient": user.is_patient,
            "blood_type": user.blood_type,
            "address": user.address,
            "email": user.email
        })
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.is_doctor:
            users = CustomUser.objects.filter(is_patient=True)
        elif current_user.is_patient:
            users = CustomUser.objects.filter(is_doctor=True)
        else:
            users = CustomUser.objects.none()

        serializer = PublicUserSerializer(users, many=True)
        return Response(serializer.data)
    

class AllUsersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        if current_user.is_patient:
            users = CustomUser.objects.filter(is_doctor=True)
        elif current_user.is_doctor:
            users = CustomUser.objects.filter(is_patient=True)
        else:
            users = CustomUser.objects.none()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class PatientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        patients = CustomUser.objects.filter(is_patient=True)
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data)