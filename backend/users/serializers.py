from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telegram_chat_id = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "telegram_chat_id")

    def create(self, validated_data):
        telegram_chat_id = validated_data.pop("telegram_chat_id", None)
        user = User.objects.create_user(**validated_data)
        if telegram_chat_id:
            user.telegram_chat_id = telegram_chat_id
            user.save()
        return user


class TelegramChatIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["telegram_chat_id"]
