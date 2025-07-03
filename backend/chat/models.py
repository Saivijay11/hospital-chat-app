from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Thread(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor_threads', on_delete=models.CASCADE)
    patient = models.ForeignKey(User, related_name='patient_threads', on_delete=models.CASCADE)

    def __str__(self):
        return f"Thread between Dr.{self.doctor.username} and {self.patient.username}"

    @staticmethod
    def get_or_create_thread(user1, user2):
        doctor = user1 if user1.is_doctor else user2
        patient = user2 if user1.is_doctor else user1
        thread, created = Thread.objects.get_or_create(doctor=doctor, patient=patient)
        return thread


class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"