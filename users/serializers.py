from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from projects.models import Project
from tasks.serializers import TaskNestedSerializer

class RegisterSerializer(serializers.ModelSerializer): # Сериализатор регистрации
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class MyTokenObtainPairSerializer(serializers.Serializer): # Сериализатор авторизации
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные") # Проверяем данные для авторизации

        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class ProjectNestedSerializer(serializers.ModelSerializer): # Сериализатор для проекта
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    tasks = TaskNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['name', 'status_display', 'tasks']

class UserSerializer(serializers.ModelSerializer): # Сериализатор пользователя с отображением ролей
    owner = serializers.SerializerMethodField()
    member = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'owner', 'member']

    def get_owner(self, obj): # Получаем связанные с юзером проекты и задачи
        projects = obj.projects.all().select_related('owner').prefetch_related('tasks')  # проекты, где пользователь - owner
        return ProjectNestedSerializer(projects, many=True, context=self.context).data

    def get_member(self, obj):
        projects = obj.member_projects.all().select_related('owner').prefetch_related('tasks')  # проекты, где пользователь - участник
        return ProjectNestedSerializer(projects, many=True, context=self.context).data