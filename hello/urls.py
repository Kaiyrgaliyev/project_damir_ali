from django.urls import path, include
from django.contrib.auth import views as auth_views
from hello import views
from hello.models import LogMessage
from django.conf import settings
from django.conf.urls.static import static

home_list_view = views.HomeListView.as_view(
    queryset=LogMessage.objects.order_by("-log_date")[:5],
    context_object_name="message_list",
    template_name="hello/home.html",
)

urlpatterns = [
    # Главная страница
    path("", home_list_view, name="home"),

    # О сайте и контакты
    path("about/", views.about, name="about"),
    
    # Сообщения
    path("log/", views.log_message_create, name="log"),  # Исправлено на log_message_create
    path("log_messages/", views.log_message_list, name="log_message_list"),
    path("log_messages/new/", views.log_message_create, name="log_message_create"),

    # Профиль
    path("profile/", views.user_profile, name="profile"),

    # Чат, категории, объявления
    path("chat/", views.chat, name="chat"),
    path("categories/", views.category_list, name="category_list"),
    path("ads/", views.ad_list, name="ad_list"),
    path('delete/<int:pk>/', views.delete_log_message, name='delete_log_message'),

    # Аутентификация
    path("login/", auth_views.LoginView.as_view(template_name="hello/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    # Капча
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчики ошибок
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'