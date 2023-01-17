from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from scenario.models import Profile


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'age',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age',)


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'social_media_link')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
           # 'profile_picture':
            'social_media_link': forms.TextInput(attrs={'class': 'form-control'})

    }
