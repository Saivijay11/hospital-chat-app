from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, ApprovedDoctor


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Admin list display for quick overview
    list_display = ('id', 'username', 'email', 'full_name', 'doctor_id', 'is_staff', 'is_superuser')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email', 'full_name', 'doctor_id')
    ordering = ('id',)

    # Fields to show/edit in the user detail page
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('full_name', 'email', 'doctor_id', 'blood_type', 'address')
        }),
    )

    # Fields to show when adding a new user from admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'full_name', 'doctor_id', 'blood_type', 'address',
                'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


class ApprovedDoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'full_name', 'verified_at')
    search_fields = ('doctor_id', 'full_name')
    ordering = ('-verified_at',)


# Register both models in admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ApprovedDoctor, ApprovedDoctorAdmin)
