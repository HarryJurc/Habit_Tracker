from django.urls import path
from .views import TelegramChatIdUpdateView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("telegram/", TelegramChatIdUpdateView.as_view(), name="telegram-chat-id"),
]
