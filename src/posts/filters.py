from dataclasses import fields
from django_filters.rest_framework import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {"user_id": ["exact"]}
