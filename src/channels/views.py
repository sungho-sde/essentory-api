from django.shortcuts import render

# Create your views here.
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Channel
from posts.models import Post
from .serializers import ChannelSerializer, ChannelAddPostSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_post':
            return ChannelAddPostSerializer
        return ChannelSerializer

    @action(detail=True, methods=["post"], url_path="posts")
    def add_post(self, request, pk=None):
        serializer = ChannelAddPostSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data["post_id"]

            # Update the post to link it to the channel specified by 'pk'
            try:
                post = Post.objects.get(id=post_id)
                post.channel_id = pk  # Set the channel ID from URL
                post.save()

                return Response({'status': 'Post={} added to channel={} successfully'.format(post_id, pk)}, status=status.HTTP_200_OK)
            except Post.DoesNotExist:
                return Response({'error': 'Post={} not found'.format(post_id)}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)