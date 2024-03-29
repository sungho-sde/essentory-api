from rest_framework import serializers
from .models import Channel, ChannelMember, Link
from posts.models import Post


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('display_name', 'url')


class ChannelSerializer(serializers.ModelSerializer):
    creators = serializers.PrimaryKeyRelatedField(queryset=ChannelMember.objects.all(), many=True)
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = "__all__"


class ChannelAddPostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    @staticmethod
    def validate_post_id(value):
        if not Post.objects.filter(id=value).exists():
            raise serializers.ValidationError("Post with ID={} does not exist.".format(value))
        return value
