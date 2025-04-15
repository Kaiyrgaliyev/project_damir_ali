from django import forms
from .models import LogMessage
from captcha.fields import CaptchaField

class LogMessageForm(forms.ModelForm):
    captcha = CaptchaField()  # Добавляем CAPTCHA

    class Meta:
        model = LogMessage
        fields = ['message', 'captcha']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 5:
            raise forms.ValidationError("Message must be at least 5 characters long.")
        return message