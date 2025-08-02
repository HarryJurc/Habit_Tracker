from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

User = get_user_model()


class TelegramChatIdUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chat_id = request.data.get("telegram_chat_id")
        if not chat_id:
            return Response({"error": "telegram_chat_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.telegram_chat_id = chat_id
        request.user.save()
        return Response({"message": "Telegram chat ID updated"}, status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)