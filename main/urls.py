# urls.py

from django.urls import path
from .views import (
    CustomUserCreate,
    CustomUserListView,
    CustomUserLogin,
    CustomUserLogout,
    CustomUserEdit,
    AuthorCreate,
    AuthorEdit,
    AuthorUpdate,
    AuthorDelete,
    AuthorDetail,
    AuthorsList,)


urlpatterns = [
    path('user/create/', CustomUserCreate.as_view(), name='customuser-create'),
    path('user/logout/', CustomUserLogout.as_view(), name='user-logout'),
    path('user/login/', CustomUserLogin.as_view(), name='user-login'),
    path('user/edit/<str:username>/', CustomUserEdit.as_view(), name='user-edit'),
    path('users/', CustomUserListView.as_view(), name='customuser-list'),
    path('author/create/', AuthorCreate.as_view(), name='author-create'),
    path('author/edit/<int:id>/', AuthorEdit.as_view(), name='author-edit'),
    path('author/update/<int:id>/', AuthorUpdate.as_view(), name='author-update'),
    path('author/delete/<int:id>/', AuthorDelete.as_view(), name='author-delete'),
    path('author/<int:id>/', AuthorDetail.as_view(), name='author-detail'),
    path('authors/', AuthorsList.as_view(), name='authors-list'),

]
