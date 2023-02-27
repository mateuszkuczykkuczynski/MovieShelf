from django import forms
from .models import WatchedByUser, ToWatchByUser


class WatchedForm(forms.ModelForm):

    class Meta:
        model = WatchedByUser
        fields = ()


class ToWatchForm(forms.ModelForm):

    class Meta:
        model = ToWatchByUser
        fields = ()
