from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    WORK_STATUS_CHOICES = [
        ('experienced', 'Experienced'),
        ('fresher', 'Fresher'),
    ]
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no', 'work_status']

    def __str__(self):
        return self.email
