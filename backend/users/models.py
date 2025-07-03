from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    address = models.TextField(blank=True)
    doctor_id = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

class ApprovedDoctor(models.Model):
    doctor_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.doctor_id})"
    
class ApprovedDoctor(models.Model):
    doctor_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.doctor_id} - {self.full_name}"
