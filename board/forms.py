from django import forms
from board.models import Advertisement, Response


class RegistrationForm(forms.Form):
    pass


class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['title', 'content', 'category']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data['text']
        # Дополнительные проверки, если необходимо
        return text
