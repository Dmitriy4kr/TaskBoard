from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectListView,
    ProjectStatusUpdateView,
    JoinUserToProjectView,
)

urlpatterns = [
    path('new-project/', ProjectCreateView.as_view(), name='project-create'), # Эндпоинт создания нового проекта
    path('', ProjectListView.as_view(), name='project-list'), # Эндпоинт списка проектов
    path('<int:pk>/status/', ProjectStatusUpdateView.as_view(), name='project-status-update'), # Эндпоинт обновления статуса проекта по id
    path('users-in/', JoinUserToProjectView.as_view(), name='project-users-in'), # Эндпоинт добавления участника к проектпо email и названию проекта
]