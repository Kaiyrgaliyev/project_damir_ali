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
    path("", home_list_view, name="home"),
    path("about/", views.about, name="about"),
    path("log/", views.log_message, name="log"),
    path("log_messages/", views.log_message_list, name="log_message_list"),
    path("log_messages/new/", views.log_message_create, name="log_message_create"),
    path('captcha/', include('captcha.urls')),
    path("profile/", views.user_profile, name="user_profile"),
    path("chat/", views.chat, name="chat"),
    path('categories/', views.category_list, name='category_list'),

    # Аутентификация
    path("login/", auth_views.LoginView.as_view(template_name="hello/login.html"), name="login"),  # Вход
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # Выход
    path("register/", views.register, name="register"),  # Регистрация
]
