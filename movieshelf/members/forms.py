from django import forms
from scenario.models import Profile


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'social_media_link')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
           # 'profile_picture':
            'social_media_link': forms.TextInput(attrs={'class': 'form-control'})

    }