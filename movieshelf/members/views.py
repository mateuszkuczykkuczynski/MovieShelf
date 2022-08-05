from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from scenario.models import Profile


class PasswordsChangeView(PasswordChangeView):
    model = Profile
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')


class ProfileDetailsView(generic.UpdateView):
    model = Profile
    template_name = 'registration/profile_details.html'
    fields = ['bio', 'profile_picture', 'social_media_link']
    success_url = reverse_lazy('homepage')


class ProfilePageView(generic.DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user


def password_success(request):
    return render(request, 'registration/password_success.html')