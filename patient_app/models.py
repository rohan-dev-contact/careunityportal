from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    mobile=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    def __str__(self):
        return ("UserName = " + self.username+", Email = "+self.email)

class Department(models.Model):
    department_name = models.CharField(max_length=255)
    work_description = models.TextField(blank=True, null=True)
    intended_patients = models.CharField(max_length=255, blank=True, null=True)
    treated_diseases = models.TextField(blank=True, null=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    special_facilities = models.TextField(blank=True, null=True)
    operating_hours = models.TextField(blank=True, null=True)
    emergency_services = models.BooleanField(default=False)
    insurance_accepted = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.department_name


class Specialization(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.ManyToManyField(Specialization)
    experience = models.IntegerField()
    departments = models.ManyToManyField(Department)
    def __str__(self):
        return (self.user.first_name+' '+self.user.last_name + ' ('+self.user.username+')')
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    health_condition = models.TextField()
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    health_insurance = models.CharField(max_length=255)    
    age = models.IntegerField(default=0)
    gender=models.CharField(max_length=255)
    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name} (ID: {self.pk})"
    


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

# class Appointment(models.Model):
#     appid=models.AutoField(primary_key=True)
#     doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Doctor')
#     patient=models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='Patient')
#     appmadeon=models.DateField(auto_now_add=True, blank=False, verbose_name='Appointment Made Date')
#     appdate=models.DateField(verbose_name='Appointment Date')
    
