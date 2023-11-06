import pytest
from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.urls import reverse
from main.views import CustomUserView, AuthorView
from main.models import CustomUser, Author
from main.serializers import CustomUserSerializer, AuthorSerializer


@pytest.mark.django_db
def test_custom_user_view_get_single_user():
    user = CustomUser.objects.create(
        username='testuser', email='test@example.com')
    factory = APIRequestFactory()
    request = factory.get('/user/testuser/')  # URL codificada diretamente

    response = CustomUserView.as_view()(request, username='testuser')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_custom_user_view_post():
    data = {'username': 'newuser',
            'email': 'newuser@example.com', 'password': 'password123', 'sex': 'Male', 'gender': 'Man'}

    factory = APIRequestFactory()
    # URL codificada diretamente
    request = factory.post('/user/', data, format='json')

    response = CustomUserView.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED

    # Adicione mais verificações conforme necessário

# Teste para a view AuthorView


@pytest.mark.django_db
def test_author_view_get_single_author():
    author = Author.objects.create(first_name='Test', last_name='Author')
    factory = APIRequestFactory()
    request = factory.get('/author/1/')  # URL codificada diretamente

    response = AuthorView.as_view()(request, id=1)
    assert response.status_code == status.HTTP_200_OK

    # Adicione mais verificações conforme necessário


@pytest.mark.django_db
def test_author_view_post():
    data = {'first_name': 'New', 'last_name': 'Author'}

    factory = APIRequestFactory()
    # URL codificada diretamente
    request = factory.post('/author/', data, format='json')

    response = AuthorView.as_view()(request)
    assert response.status_code == status.HTTP_201_CREATED
