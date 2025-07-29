from django.urls import path
from users.views import RegisterView, MyTokenObtainPairView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # Эндпоинт регистрации
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # Эндпоинт авторизации
    path('all/', UserListView.as_view(), name='user-list'), # Эндпоинт для показа всех юзеров
]
