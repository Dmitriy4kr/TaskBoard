from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager): # Кастомный способ создания юзера
    def create_user(self, email, password=None, username=None):
        if not email:
            raise ValueError('Email обязателен') # Указываем, что email является обязательным для идентификации юзера

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.role = 'owner' # Указываем, что каждый регистрируемый юзер будет владелец проекта
        user.save(using=self._db)
        return user

class User(AbstractUser): # Модель юзера со своими настройками
    email = models.EmailField(unique=True) # Как логин используем email
    role = models.CharField(max_length=20, choices=[('owner', 'Owner'), ('member', 'Member')], default='owner')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
