from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User
from .models import LogMessage
from django.test import TestCase
from .models import Category, Ad

class TestLogMessageModel(TestCase):

    def setUp(self):
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Создаём объект LogMessage
        self.log_message = LogMessage.objects.create(
            user=self.user,  # Передаём пользователя
            message='Test Message',
            log_date=timezone.now()
        )

    def test_log_message_creation(self):
        # Проверяем, что объект LogMessage создан
        self.assertTrue(isinstance(self.log_message, LogMessage))
        self.assertEqual(self.log_message.message, 'Test Message')

    def test_log_message_str(self):
        # Проверяем строковое представление объекта LogMessage
        expected_object_name = f"'{self.log_message.message}' logged on {timezone.localtime(self.log_message.log_date).strftime('%A, %d %B, %Y at %X')}"
        self.assertEqual(str(self.log_message), expected_object_name)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_not_found_url(self):
        # Проверяем, что несуществующий URL возвращает 404
        response = self.client.get('/a-url-that-does-not-exist')
        self.assertEqual(response.status_code, 404)  # Исправлено с assertEquals на assertEqual

    
class TestAdListView(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test Description",
            category=self.category,
            is_promoted=True
        )

    def test_ad_list_view(self):
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ad")