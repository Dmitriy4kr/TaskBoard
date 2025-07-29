from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Project
from .serializers import (
    ProjectSerializer,
    ProjectStatusSerializer,
    JoinUserToProjectSerializer,
)
from users.serializers import TaskNestedSerializer

User = get_user_model()

# Создание проекта
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

# Список проектов текущего пользователя (под кем авторизован)
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

# Обновление статуса проекта
class ProjectStatusUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

# Присоединение пользователя по названию проекта и email
class JoinUserToProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = JoinUserToProjectSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project = serializer.validated_data['project']
        user = serializer.validated_data['user']

        # Проверка прав доступа (только владелец)
        if project.owner != request.user:
            return Response({'detail': 'У вас нет прав на изменение этого проекта.'}, status=status.HTTP_403_FORBIDDEN)

        # Проверка, есть ли уже участник
        if user in project.members.all():
            return Response({'detail': 'Пользователь уже участник проекта.'}, status=status.HTTP_400_BAD_REQUEST)

        # Добавляем пользователя к проекту
        project.members.add(user)
        return Response({'detail': f'Пользователь {user.email} успешно добавлен к проекту "{project.name}".'})