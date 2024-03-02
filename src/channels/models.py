from django.db import models
from accounts.models import User


class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(
        User,
        related_name="owned_channels",
        on_delete=models.CASCADE,
    )
    managers = models.ManyToManyField(User, related_name="managed_channels")
    subscribers = models.ManyToManyField(User, related_name="subscribed_channels")
    created_at = models.DateTimeField(auto_now_add=True)
