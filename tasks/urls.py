from django.urls import path
from .views import TaskCreateView, TaskListView, TaskStatusUpdateView, CommentListCreateView

urlpatterns = [
    path('new-task/', TaskCreateView.as_view(), name='task-create'), # Эндпоинт для создания новой задачи
    path('', TaskListView.as_view(), name='task-list'), # Эндпоинт для получения списка всех задач
    path('<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task-status-update'), # Эндпоинт для обновления статуса задачи по id
    path('<int:task_id>/comments/', CommentListCreateView.as_view(), name='task-comments'), # Эндпоинт для добавления комментариев к задаче
]
