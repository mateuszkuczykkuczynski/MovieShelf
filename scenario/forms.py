from django import forms
from .models import WatchedByUser, ToWatchByUser, MovieShelfRating
from django.core.validators import MinValueValidator, MaxValueValidator


class WatchedForm(forms.ModelForm):
    class Meta:
        model = WatchedByUser
        fields = ()


class ToWatchForm(forms.ModelForm):
    class Meta:
        model = ToWatchByUser
        fields = ()


class MovieShelfRatingsForm(forms.ModelForm):
    rating = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        model = MovieShelfRating
        fields = ('rating',)

    # def __init__(self, *args, **kwargs):
    #     super(MovieShelfRatingsForm, self).__init__(*args, **kwargs)
    #     self.fields['rating'].widget = forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
