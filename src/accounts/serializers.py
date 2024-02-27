from rest_framework.serializers import ModelSerializer
from .models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify the fields you want to include in your serializer
        # Typically, you'll exclude sensitive fields like 'password'
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
        ]
        read_only_fields = [
            "id",
        ]  # Fields that should not be updated directly

    # If you want to handle password updates or set the password for new users,
    # you can define a custom method to do so, ensuring to hash the password correctly.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Manually handle the update for each field you want to allow updates for
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.profile_picture = validated_data.get(
            "profile_picture", instance.profile_picture
        )
        # Ensure to save the updated instance
        instance.save()
        return instance
