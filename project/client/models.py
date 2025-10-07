from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here
from .managers import CustomUserManager

#DONE add description
class Client(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    name = models.CharField(blank=True, null=True)
    surname = models.CharField(blank=True, null=True)
    address = models.CharField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    file_groups = models.JSONField(default=list)
    user_id = models.UUIDField(default = uuid.uuid4)
    verification_id = models.UUIDField(default=uuid.uuid4)
    is_verified = models.BooleanField(default=False)
    description = models.CharField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email