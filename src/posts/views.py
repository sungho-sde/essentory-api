from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter

from posts.filters import PostFilter
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# Controller
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PostFilter
    search_fields = ["text"]
    ordering_fileds = []


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs["post_pk"])
        return super().get_queryset()

    def get_serializer_context(self):
        return {"post_id": self.kwargs["post_pk"]}
