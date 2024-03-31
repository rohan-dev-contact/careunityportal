from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    mobile=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
    def __str__(self):
        return ("UserName = " + self.username+", Email = "+self.email)

class Department(models.Model):
    department_name=models.CharField(max_length=255)
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

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    health_condition = models.TextField()
    assigned_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    health_insurance = models.CharField(max_length=255)    
    date_of_birth = models.DateField(default=datetime.date(2000, 1, 1))
    gender=models.CharField(max_length=255)