from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom manager for handling user creation with email instead of username
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        
        # Normalize the email address
        email = self.normalize_email(email)

        # Create user instance with provided fields
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)    # Save user to the database
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create a regular user (non-staff, non-superuser).
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create a superuser with staff and superuser privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Validate that the required flags are set for superuser
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, **extra_fields)


# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    # Override username field to make it optional and not unique
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,      # Not used for authentication
        blank=True,        # Can be left blank
        null=True,         # Can be null in DB
        help_text=_("Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    # Additional fields
    name = models.CharField(max_length=150)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Email is used as unique identifier for login

    # Work status options
    WORK_STATUS_CHOICES = [
        ('experienced', 'Experienced'),
        ('fresher', 'Fresher'),
    ]
    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, blank=False)

    # Use email instead of username for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile_no', 'work_status']  # Required when creating superuser via createsuperuser

    # Assign custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.email  