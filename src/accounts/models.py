from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uid = models.CharField(max_length=255, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    push_token = models.CharField(max_length=255, blank=True, null=True)
