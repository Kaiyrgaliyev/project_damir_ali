from django.urls import path, include
from django.contrib.auth import views as auth_views
from hello import views
from hello.models import LogMessage

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],  # :5 limits the results to the five most recent
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    path("", home_list_view, name="home"),  # Главная страница
    path("about/", views.about, name="about"),  # Страница "О нас"
    path("log/", views.log_message, name="log"),  # Форма логирования
    path("log_messages/", views.log_message_list, name="log_message_list"),  # Список сообщений
    path("log_messages/new/", views.log_message_create, name="log_message_create"),  # Создание нового сообщения
    path('captcha/', include('captcha.urls')),  # Добавляем маршруты для CAPTCHA
    path("profile/", views.user_profile, name="user_profile"),  # Личный кабинет
    path("chat/", views.chat, name="chat"),  # Чат

    # Аутентификация
    path("login/", auth_views.LoginView.as_view(template_name="hello/login.html"), name="login"),  # Вход
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # Выход
    path("register/", views.register, name="register"),  # Регистрация
]
