from django.utils.timezone import datetime
from django.shortcuts import render, redirect, get_object_or_404
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Category
from .models import Ad
from .models import Review
from datetime import datetime
from django import forms
from .models import LogMessage
from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib.auth.models import User

def delete_log_message(request, pk):
    message = get_object_or_404(LogMessage, pk=pk)
    if request.method == "POST":
        message.delete()
        return redirect('log_message_list')
    return render(request, 'hello/confirm_delete.html', {'message': message})


def profile(request):
    # Здесь ты можешь передать информацию о пользователе
    return render(request, 'profile.html', {
        'user': request.user,
        # Другие данные для профиля
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'hello/category_list.html', {'categories': categories})

@login_required
def chat(request):
    """Отображает чат пользователя."""
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        content = request.POST.get('content')
        try:
            recipient = User.objects.get(username=recipient_username)
            ChatMessage.objects.create(sender=request.user, recipient=recipient, content=content)
        except User.DoesNotExist:
            return render(request, 'hello/chat.html', {'error': 'Recipient does not exist.'})

    messages = ChatMessage.objects.filter(recipient=request.user) | ChatMessage.objects.filter(sender=request.user)
    messages = messages.order_by('-timestamp')
    return render(request, 'hello/chat.html', {'messages': messages})

@login_required
def user_profile(request):
    """Отображает личный кабинет пользователя."""
    user_messages = LogMessage.objects.filter(user=request.user)  # Сообщения текущего пользователя
    return render(request, 'hello/user_profile.html', {'user_messages': user_messages})

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage
    queryset = LogMessage.objects.order_by("-log_date")[:5]  # Ограничиваем до 5 последних сообщений
    context_object_name = "message_list"
    template_name = "hello/home.html"


def about(request):
    """Renders the about page."""
    return render(request, "hello/about.html")


def log_message_list(request):
    """Displays a list of all log messages with search functionality."""
    query = request.GET.get('q', '')  # Получаем поисковый запрос из параметров URL
    if query:
        messages = LogMessage.objects.filter(message__icontains=query)  # Фильтрация по тексту
    else:
        messages = LogMessage.objects.all()
    return render(request, 'hello/log_message_list.html', {'messages': messages, 'query': query})

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ['message', 'image']

def log_message_create(request):
    """Creates a new log message."""
    if request.method == 'POST':
        form = LogMessageForm(request.POST, request.FILES)  # Добавлено request.FILES
        if form.is_valid():
            log_message = form.save(commit=False)
            log_message.user = request.user
            log_message.save()
            return redirect('log_message_list')
    else:
        form = LogMessageForm()
    return render(request, 'hello/log_message_create.html', {'form': form})

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Получаем данные из POST запроса
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу
        else:
            # Если форма невалидна, ошибки будут отображаться в шаблоне
            return render(request, 'hello/register.html', {'form': form})  # Отправляем обратно форму с ошибками
    else:
        form = UserCreationForm()  # Создаем пустую форму при GET запросе
        return render(request, 'hello/register.html', {'form': form})

def ad_list(request):
    category_id = request.GET.get('category')
    is_promoted = request.GET.get('is_promoted') == '1'

    ads = Ad.objects.all()
    if category_id:
        ads = ads.filter(category_id=category_id)
    if is_promoted:
        ads = ads.filter(is_promoted=True)

    categories = Category.objects.all()
    return render(request, 'hello/ad_list.html', {'ads': ads, 'categories': categories})

@login_required
def user_profile(request):
    """Отображает личный кабинет пользователя."""
    user_messages = LogMessage.objects.filter(user=request.user)
    reviews = Review.objects.filter(reviewed_user=request.user)
    return render(request, 'hello/user_profile.html', {'user_messages': user_messages, 'reviews': reviews})