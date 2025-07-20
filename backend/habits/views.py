from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnlyPublic
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class HabitPagination(PageNumberPagination):
    page_size = 5


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyPublic]

    def get_queryset(self):
        return Habit.objects.all().order_by("id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        if request.query_params.get("public") == "true":
            queryset = self.get_queryset().filter(is_public=True).order_by("id")
        else:
            queryset = self.get_queryset().filter(user=request.user).order_by("id")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
