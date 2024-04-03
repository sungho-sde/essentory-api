from django.db import transaction
from rest_framework import serializers

from accounts.models import User
from posts.models import Post

from .models import Channel, ChannelMember, Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "display_name", "url"]
        read_only_fields = ["id"]


class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    # channel_links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = [
            "id",
            "name",
            "description",
            "owner",
            "category",
            "profile_picture_url",
            "cover_picture_url",
            "created_at",
            "updated_at",
            # "channel_links",
            # "channel_members",
        ]
        read_only_fields = (
            "total_subscribers_count",
            "total_posts_count",
        )
        extra_kwargs = {
            "owner": {"write_only": True},
        }

    def create(self, validated_data):
        channel_owner = validated_data.get("owner")
        with transaction.atomic():
            channel = Channel.objects.create(**validated_data)

            ChannelMember.objects.create(
                channel=channel, user=channel_owner, is_owner=True
            )
            return channel


class ChannelMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelMember
        fields = "__all__"


class ChannelAddPostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    @staticmethod
    def validate_post_id(value):
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "Post with ID={} does not exist.".format(value)
            )
        return value
