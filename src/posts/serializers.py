from rest_framework.serializers import ModelSerializer
from .models import Comment, Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "channel", "content", "created_at"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "post", "user", "parent_comment", "content", "created_at"]

    def create(self, validated_data):
        post_id = self.context["post_id"]
        return Comment.objects.create(post_id=post_id, **validated_data)
