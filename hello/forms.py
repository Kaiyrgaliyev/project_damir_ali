from django import forms
from .models import LogMessage
from captcha.fields import CaptchaField

class LogMessageForm(forms.ModelForm):
    captcha = CaptchaField()  # Добавляем CAPTCHA

    class Meta:
        model = LogMessage
        fields = ['message', 'image', 'video', 'video_url']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
            'video_url': forms.URLInput(attrs={'placeholder': 'https://youtube.com/...'})
        }
        labels = {
            'video_url': 'YouTube/Vimeo ссылка'
        }

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 5:
            raise forms.ValidationError("Message must be at least 5 characters long.")
        return message
    