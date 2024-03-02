from rest_framework import serializers
from yaml import serialize

# from posts import serializers
from .models import User, Device


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "username",
            "display_name",
            "email",
            "profile_picture_url",
            "status",
            "created_at",
        ]
        extra_kwargs = {
            "display_name": {"required": False, "allow_blank": True},
            "profile_picture_url": {"required": False, "allow_blank": True},
        }

        read_only_fields = [
            "uid",
        ]  # Fields that should not be updated directly

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["id", "user", "device_id", "push_token"]
        read_only_fields = ("user",)  # Assuming user is automatically assigned

    def create(self, validated_data):
        user = self.context["request"].user
        device_id = validated_data.get("device_id")
        push_token = validated_data.get("push_token")

        # Check if device already exists for the user and update push token
        device, created = Device.objects.update_or_create(
            user=user,
            device_id=device_id,
            defaults={"push_token": push_token},
        )
        return device

    def update(self, instance, validated_data):
        instance.push_token = validated_data.get("push_token", instance.push_token)
        instance.save()
        return instance

    # # If you want to handle password updates or set the password for new users,
    # # you can define a custom method to do so, ensuring to hash the password correctly.
    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user

    # def update(self, instance, validated_data):
    #     # Manually handle the update for each field you want to allow updates for
    #     instance.email = validated_data.get("email", instance.email)
    #     instance.first_name = validated_data.get("first_name", instance.first_name)
    #     instance.last_name = validated_data.get("last_name", instance.last_name)
    #     instance.profile_picture = validated_data.get(
    #         "profile_picture", instance.profile_picture
    #     )
    #     # Ensure to save the updated instance
    #     instance.save()
    #     return instance
