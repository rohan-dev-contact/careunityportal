from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile=models.CharField(max_length=15)
    address=models.CharField(max_length=255)
