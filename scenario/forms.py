from django import forms
from .models import WatchedByUser


class WatchedForm(forms.ModelForm):

    class Meta:
        model = WatchedByUser
        fields = ('watched',)


