from django.urls import path
from .views import (
    UserSignUpView,
    CreateProfileView,
    UpdateProfileView,
    DeleteProfileView,
    ProfileDetailsView,
    ProfileListView,
)

urlpatterns = [
    path('sign_up/', UserSignUpView.as_view(), name='sign_up'),
    path('create_user_profile/', CreateProfileView.as_view(), name='create_user_profile'),
    path('update_user_profile/<int:pk>/', UpdateProfileView.as_view(), name='update_user_profile'),
    path('delete_user_profile/<int:pk>/', DeleteProfileView.as_view(), name='delete_user_profile'),
    path('user_profile/<int:pk>/', ProfileDetailsView.as_view(), name='user_profile'),
    path('users_profiles_list/', ProfileListView.as_view(), name='users_profiles_list'),
]
