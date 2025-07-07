from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

#here we are creating custom admin config for the customuser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser #it specifies how admin manages the model
    #this fields will be displayed in the user list on adin panel
    list_display = ('id', 'username', 'email', 'is_doctor', 'is_patient', 'is_staff')
    search_fields = ('username', 'email') #we can search using username and email 
    ordering = ('id',) # we will sort the list by using the ids
    #adding custom fields to the default admin fileds like full name, doctorid etc.,
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'doctor_id', 'blood_type', 'address', 'is_doctor', 'is_patient')}),
    )
#we register created or customized user admin with the site
admin.site.register(CustomUser, CustomUserAdmin)