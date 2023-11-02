# urls.py

from django.urls import path
from .views import (
    CustomUserView,
    CustomUserLogin,
    CustomUserLogout,
    AuthorView,)


urlpatterns = [
    path('user/', CustomUserView.as_view(), name='customuser'),
    path('user/logout/', CustomUserLogout.as_view(), name='user-logout'),
    path('user/login/', CustomUserLogin.as_view(), name='user-login'),
    path('user/<str:username>/', CustomUserView.as_view(), name='user-edit'),
    path('author/', AuthorView.as_view(), name='author-create'),
    path('author/<int:id>/', AuthorView.as_view(), name='author-detail'),

]
