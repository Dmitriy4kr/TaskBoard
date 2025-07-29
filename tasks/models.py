from django.db import models
from projects.models import Project
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = Project.STATUS_CHOICES 

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
    
class Comment(models.Model):
    # Связь комментария с конкретной задачей
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    # Автор комментария — пользователь
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    # Текст комментария
    text = models.TextField()
    

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.name} at {self.created_at}"
