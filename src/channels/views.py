from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from posts.models import Post

from .models import Channel, ChannelMember, Link
from .serializers import (
    ChannelAddPostSerializer,
    ChannelMemberSerializer,
    ChannelSerializer,
    LinkSerializer,
)


class ChannelViewSet(ModelViewSet):
    queryset = Channel.objects.all()

    def get_serializer_class(self):
        if self.action == "add_post":
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

                return Response(
                    {
                        "status": "Post={} added to channel={} successfully".format(
                            post_id, pk
                        )
                    },
                    status=status.HTTP_200_OK,
                )
            except Post.DoesNotExist:
                return Response(
                    {"error": "Post={} not found".format(post_id)},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChannelMemberViewSet(ModelViewSet):
    queryset = ChannelMember.objects.all()
    serializer_class = ChannelMemberSerializer

    def get_queryset(self):
        return ChannelMember.objects.filter(channel_id=self.kwargs["channel_pk"])


class LinkViewSet(ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def get_queryset(self):
        channel_pk = self.kwargs.get("channel_pk")
        get_object_or_404(Channel, pk=channel_pk)
        return Link.objects.filter(channel_id=channel_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["channel_pk"] = self.kwargs["channel_pk"]
        return context

    def perform_create(self, serializer):
        channel_pk = self.kwargs.get("channel_pk")
        channel = get_object_or_404(Channel, pk=channel_pk)
        serializer.save(channel=channel)
