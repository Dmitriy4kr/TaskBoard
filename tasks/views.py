from rest_framework import generics, permissions
from .models import Task, Comment
from .serializers import TaskSerializer, TaskStatusSerializer, CommentSerializer
from django.shortcuts import get_object_or_404


class TaskCreateView(generics.CreateAPIView): # View для создания задачи
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)

class TaskListView(generics.ListAPIView): # View для получения списка задач
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.select_related('project').prefetch_related('comments', 'project__owner')

class TaskStatusUpdateView(generics.UpdateAPIView): # View для обновления статуса задачи
    serializer_class = TaskStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
class CommentListCreateView(generics.ListCreateAPIView): # View для просмотра и добавления комментариев
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получение комментариев только для указанной задачи
        task_id = self.kwargs['task_id']
        return Comment.objects.filter(task_id=task_id).order_by('created_at')

    def perform_create(self, serializer):
        # При создании комментария привязывать его к текущему пользователю и задаче
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Task, id=task_id)
        serializer.save(author=self.request.user, task=task)
