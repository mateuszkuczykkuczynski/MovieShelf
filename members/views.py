from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from .models import UserProfile


from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.views import PasswordChangeView
# from scenario.models import Profile
# from .forms import ProfilePageForm


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
    success_url = reverse_lazy('user_profile_details')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class DeleteProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserProfile
    template_name = 'delete_user_profile.html'
    success_url = reverse_lazy('user_profile_details')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'user_profile_details.html'


# class ProfilePageView(generic.DetailView):
#     model = Profile
#     template_name = 'registration/user_profile.html'
#
#     def get_context_data(self, *args, **kwargs):
#         users = Profile.objects.all()
#         context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
#
#         page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
#
#         context["page_user"] = page_user
#         return context

