# urls.py

from django.urls import path
from .views import CustomUserCreate, CustomUserListView, CustomUserLogin, CustomUserLogout, CustomUserEdit

urlpatterns = [
    path('user/create/', CustomUserCreate.as_view(), name='customuser-create'),
    path('user/logout/', CustomUserLogout.as_view(), name='user-logout'),
    path('user/login/', CustomUserLogin.as_view(), name='user-login'),
    path('user/edit/<str:username>/', CustomUserEdit.as_view(), name='user-edit'),
    path('users/', CustomUserListView.as_view(), name='customuser-list'),

]
