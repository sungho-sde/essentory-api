from django.db import models
from posts.models import Post


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    media_type = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
