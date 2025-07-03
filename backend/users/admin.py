from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'username', 'email', 'is_doctor', 'is_patient', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('id',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'doctor_id', 'blood_type', 'address', 'is_doctor', 'is_patient')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
