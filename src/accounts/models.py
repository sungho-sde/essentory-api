from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

STATUS_CHOICES = [
    ("Active", "Active"),
    ("Inactive", "Inactive"),  # Deactivated?
    ("Suspended", "Suspended"),
]


# class AuthUser(models.Model):
#     uid = models.CharField(primary_key=True, max_length=255, unique=True, blank=False)


class User(AbstractUser):
    # auth_user = models.On2eToOneField(
    #     AuthUser, on_delete=models.CASCADE, related_name="profile"
    # )
    # id = models.AutoField(primary_key=True)
    id = ShortUUIDField(
        length=12,
        max_length=40,
        primary_key=True,
    )
    uid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    username = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(_("display name"), max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Active")
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_id = models.CharField(max_length=255)
    push_token = models.CharField(max_length=255, blank=True, null=True)
