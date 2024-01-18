from django.db import models
from accounts.models import User


class Channel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owners = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
