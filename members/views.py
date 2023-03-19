from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render

from .forms import CustomUserCreationForm
from .models import UserProfile


class UserSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class CreateProfileView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name = "create_user_profile.html"
    fields = ['avatar', 'socials', 'bio']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    template_name = 'edit_user_profile.html'
    fields = ['avatar', 'socials', 'bio']

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'pk': self.object.pk})


class DeleteProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProfile
    template_name = 'delete_user_profile.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('create_user_profile')


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile_details.html'

    def get(self, request, **kwargs):

        profile = get_object_or_404(UserProfile, pk=kwargs.get('pk'))
        context = {'profile': profile}
        return render(request, self.template_name, context)


class ProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'user_profiles_list.html'
    context_object_name = 'all_users_profiles'
