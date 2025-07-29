from rest_framework import serializers
from .models import Task, Comment
from projects.models import Project

# Сериализатор комментариев
class CommentNestedSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True) # Будет отображаться имя юзера, а не id

    class Meta:
        model = Comment
        fields = ['text', 'author'] # Говорим, чтобы показывался только текст и имя юзера

# Сериализатор задачи
class TaskSerializer(serializers.ModelSerializer):
    # project = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Project.objects.all())
    project_name = serializers.CharField(source='project.name', read_only=True)
    title = serializers.CharField(source='name')
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES, write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    comments_texts = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['project', 'project_name', 'title', 'status', 'status_display', 'comments_texts']

    def validate_project(self, value): # Делаем ограничение на то, чтобы юзер мог создавать задачу только в своем проекте
        user = self.context['request'].user
        if value.owner != user:
            raise serializers.ValidationError("Вы можете добавлять задачи только к своим проектам.")
        return value

    def get_comments_texts(self, obj):
        return [comment.text for comment in obj.comments.all()]

# Для обновления только статуса задачи
class TaskStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Task.STATUS_CHOICES, write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = ['status', 'status_display']

# Сериализатор задач с комментариями
class TaskNestedSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    comments = CommentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['name', 'status_display', 'comments']

# Сериализатор комментария (для создания)
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    #created_at = serializers.ReadOnlyField()
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    project_name = serializers.CharField(source='task.project.name', read_only=True)
    task_name = serializers.CharField(source='task.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['task', 'project_name', 'task_name', 'author', 'text']
        read_only_fields = ['author', 'project_name', 'task_name']
