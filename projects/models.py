from django.db import models
from django.conf import settings

class Project(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новые'),
        ('in_progress', 'В работе'),
        ('testing', 'Тестируется'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'), # Статусы проекта
    ]

    owner = models.ForeignKey(                  # Владелец проекта со связью у одного проекта - один владелец
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    
    members = models.ManyToManyField(            # Участники проекта со связью, что юзер может быть участником многих проектов 
        settings.AUTH_USER_MODEL,
        related_name='member_projects',
        blank=True 
    )
    
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new') # по умолчанию созданный проект имеет статус Новые

    class Meta:
        unique_together = ('owner', 'name') # Поля owner и name должны быть уникальной во всей таблице в БД

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"
