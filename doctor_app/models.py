from django.db import models
from patient_app.models import User,Patient
from django.utils import timezone

class Prescription(models.Model):
    pres_id = models.CharField(max_length=10)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.CharField(max_length=255)
    instructions = models.TextField()
    diagnosis = models.TextField(blank=True)
    general_info = models.TextField(blank=True)
    follow_up = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)

    # def __str__(self):
    #     return f"Prescription ID: {self.id}"

class Document(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title