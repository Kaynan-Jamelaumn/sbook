# urls.py

from django.urls import path
from .views import (
    CurrentUserView,
    CustomUserView,
    CustomUserLogin,
    CustomUserLogout,
    AuthorView,)


urlpatterns = [
    path('user/current/', CurrentUserView.as_view(), name='current-user'),
    path('user/', CustomUserView.as_view(), name='user'),
    path('user/logout/', CustomUserLogout.as_view(), name='user-logout'),
    path('user/login/', CustomUserLogin.as_view(), name='user-login'),
    path('user/<int:id>/', CustomUserView.as_view(), name='user-edit'),

    path('author/', AuthorView.as_view(), name='author'),
    path('author/<int:pk>/', AuthorView.as_view(), name='author-detail'),

]
