from django.urls import path
from .views import UserRegisterView, UserEditView, ProfilePageView, ProfileDetailsView, \
    PasswordsChangeView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('<int:pk>/edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('<int:pk>/profile/', ProfilePageView.as_view(), name='user_profile_page'),
    path('<int:pk>/profile_details/', ProfileDetailsView.as_view(), name='profile_details'),
    path('create_profile_page', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('<int:pk>/password/', PasswordsChangeView.as_view(template_name='registration/change_password.html')),
    path('password_success', views.password_success, name='password_success'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_form.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name="password_reset_complete"),


]