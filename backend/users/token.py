from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# This is my custom JWT serializer.
# I'm extending the default TokenObtainPairSerializer so I can include extra user info in the token payload.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        # First, call the default method to generate the token
        token = super().get_token(user)

        # Then I added ncustom fields to the token which helps on the frontend part
        token['user_id'] = user.id
        token['username'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient

        return token

# This is the view that replaces the default JWT login endpoint
# I plugged in my custom serializer above so it returns role-based info with the token
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
