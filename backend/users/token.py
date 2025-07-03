from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient
        return token

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
