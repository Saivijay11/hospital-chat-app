from django.apps import AppConfig

class UsersConfig(AppConfig): #user apps config class
    default_auto_field = "django.db.models.BigAutoField" #setting the primary key for models 
    name = "users" # registering the app unser the user