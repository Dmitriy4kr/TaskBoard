from rest_framework import serializers
from .models import Project
from users.serializers import TaskNestedSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Присоединение пользователя по email к проекту по названию проекта
class JoinUserToProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField()
    user_email = serializers.EmailField()

    def validate(self, data):
        # Проверка существования проекта по названию
        try:
            project = Project.objects.get(name=data['project_name'])
        except Project.DoesNotExist:
            raise serializers.ValidationError({"project_name": "Проект с таким названием не найден."})
        data['project'] = project

        # Проверка существования пользователя по email
        try:
            user = User.objects.get(email=data['user_email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_email": "Пользователь с таким email не найден."})
        data['user'] = user

        return data

    def save(self):
        validated_data = self.validated_data
        project = validated_data['project']
        user = validated_data['user']
        project.members.add(user)
        project.save()
        return project

class ProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'status_display', 'tasks']

    def validate_name(self, value):
        user = self.context['request'].user
        if Project.objects.filter(owner=user, name=value).exists():
            raise serializers.ValidationError("Проект с таким названием уже существует.")
        return value

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class ProjectStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Project
        fields = ['status_display']