from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model used for authentication. and no role based logins 
    Additional profile data is included for potential doctor verification or chat context.
    """
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    address = models.TextField(blank=True)
    doctor_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional. Used only if the user is a doctor and applies for verification."
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # email is now the primary login field

    class Meta:
        db_table = 'custom_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.full_name or self.username


class ApprovedDoctor(models.Model):
    """
    ApprovedDoctor stores doctor identities that have been admin-verified.
    This does not impact login. It's used for optional vetting or UI differentiation.
    """
    doctor_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    verified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'approved_doctor'
        verbose_name = 'Approved Doctor'
        verbose_name_plural = 'Approved Doctors'

    def __str__(self):
        return f"{self.full_name} ({self.doctor_id})"
