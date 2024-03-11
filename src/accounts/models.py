from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'), # Deactivated?
        ('Suspended', 'Suspended'),
    ]

    uid = models.CharField(primary_key=True, max_length=255, unique=True, null=False, blank=False)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(_("display name"), max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    push_token = models.CharField(max_length=255, blank=True, null=True)
