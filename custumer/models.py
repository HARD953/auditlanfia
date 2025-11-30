# api/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, default="issa")
    start_date = models.DateTimeField(default=timezone.now)
    adresse = models.CharField(max_length=300, blank=True, null=True)
    create = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=True)
    is_entreprise = models.BooleanField(default=True)
    is_recenseur = models.BooleanField(default=False)
    is_lanfia = models.BooleanField(default=True)
    is_user = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now())
    district = models.CharField(max_length=100, blank=False)
    region = models.CharField(max_length=100, blank=False)
    departement = models.CharField(max_length=100, blank=False)
    sous_prefecture = models.CharField(max_length=100, blank=False)
    commune = models.CharField(max_length=100, blank=False)
    entreprise=models.CharField(max_length=300, blank=True, null=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['entreprise']

    def __str__(self):
        return self.email
    # class Meta:
    #     permissions = [
    #         ("view_customUser", "Can view customUser"),
    #         ("add_customUser", "Can add customUser"),
    #         ("change_customUser", "Can change customUser"),
    #         ("delete_customUser", "Can delete customUser"),
    #     ]
