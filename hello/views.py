from django.utils.timezone import datetime
from django.shortcuts import render, redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Category
from .models import Ad
from .models import Review

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


def log_message(request):
    """Handles the log message form."""
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    return render(request, "hello/log_message.html", {"form": form})


def log_message_list(request):
    """Displays a list of all log messages with search functionality."""
    query = request.GET.get('q', '')  # Получаем поисковый запрос из параметров URL
    if query:
        messages = LogMessage.objects.filter(message__icontains=query)  # Фильтрация по тексту
    else:
        messages = LogMessage.objects.all()
    return render(request, 'hello/log_message_list.html', {'messages': messages, 'query': query})

def register(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = UserCreationForm()
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

@login_required
def log_message_create(request):
    if request.method == 'POST':
        form = LogMessageForm(request.POST, request.FILES)
        if form.is_valid():
            log_message = form.save(commit=False)  # Не сохраняем сразу в БД
            log_message.user = request.user  # Привязываем текущего пользователя
            log_message.save()  # Теперь сохраняем с пользователем
            return redirect('log_message_list')  # Перенаправляем после успеха
    else:
        form = LogMessageForm()
    
    return render(request, 'hello/log_message_create.html', {'form': form})