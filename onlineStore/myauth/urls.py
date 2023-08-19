from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import path

from .views import index, RegisterView, ProfileView, ProfileEditView, ProfileDeleteView, ChatView

app_name = 'myauth'
urlpatterns = [
    path('', index, name='main'),
    path('login/', LoginView.as_view(
        template_name='myauth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='edit'),
    path('profile/<int:pk>/change_password/',
         PasswordChangeView.as_view(template_name="myauth/profile_change_password.html"), name='change_password'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='delete'),
    path('profile/<int:pk>/chat/', ChatView.as_view(), name='chat'),
    path('profile/exit/', LogoutView.as_view(), name='exit'),
]
