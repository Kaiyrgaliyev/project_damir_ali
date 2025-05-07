from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("hello.urls")),  # Подключение маршрутов приложения hello
    path('admin/', admin.site.urls),
]

# Добавление маршрутов для статических файлов
urlpatterns += staticfiles_urlpatterns()

# Добавление маршрутов для медиафайлов (только в режиме DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)