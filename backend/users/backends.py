from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser

class CustomAuthBackend(ModelBackend):
#custom authentication for allowing login by using mail or username 
    def authenticate(self, request, username=None, password=None, **kwargs): #ovveride method for authentication
        try:
            user = CustomUser.objects.get(email=username) #here 1st try to fetch user using mail
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(username=username) # if not found by mail we do it by username
            except CustomUser.DoesNotExist:
                # if not found by using both returns none or autentication failed
                return None

        if user.check_password(password): # will check if passowrd is crrt, if wrong returns none or fails 
            return user
        return None
