from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('1-2 years', '1-2 Years'),
        ('3-5 years', '3-5 Years'),
        ('5+ years', '5+ Years'),
    ]

    EDUCATION_CHOICES = [
    ("highschool", "High School"),
    ("diploma", "Diploma"),
    ("bachelors", "Bachelor's"),
    ("masters", "Master's"),
    ("phd", "PhD"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=False, null=False)
    dob = models.DateField(null=True, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    work_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='fresher')
    skills = models.JSONField(default=list)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  

    def __str__(self):
        return f"{self.user.name}'s Profile"
