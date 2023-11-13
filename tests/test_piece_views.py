import pytest
from rest_framework.test import APIRequestFactory
from piece.views import GenreView, PublisherView
from piece.serializers import GenreSerializer, PublisherSerializer
from piece.models import Genre, Publisher
from django.urls import reverse

# APIRequestFactory é uma ferramenta fornecida pelo Django Rest Framework para ajudar na criação de solicitações HTTP em testes de API. Ela permite criar objetos de solicitação, como GET, POST, PUT, DELETE etc., simulando as requisições feitas por clientes para as vistas (views) da API. Isso é útil para testar views baseadas em funções ou classes, permitindo criar solicitações simuladas para as views do Django Rest Framework e analisar as respostas retornadas.


@pytest.mark.django_db
def test_genre_view_get():
    # Crie um objeto Genre para testar a visualização
    genre = Genre.objects.create(name='Test Genre')

    # Crie um request mock
    factory = APIRequestFactory()
    request = factory.get('/genre/')

    # Acesse a view com o método GET passando o ID do gênero
    response = GenreView.as_view()(request, pk=genre.name)
    assert response.status_code == 200  # Verifique se a resposta é bem-sucedida


@pytest.mark.django_db
def test_genre_view_get_failed():

    # Crie um request mock
    factory = APIRequestFactory()
    request = factory.get('/genre/')

    # Acesse a view com o método GET passando o ID do gênero
    response = GenreView.as_view()(request, pk='Test Genre')
    assert response.status_code == 200  # Verifique se a resposta é bem-sucedida


@pytest.mark.django_db
def test_genre_view_post():
    data = {'name': 'New Genre'}

    factory = APIRequestFactory()
    # Defina o formato como JSON
    request = factory.post('/genre/', data, format='json')

    response = GenreView.as_view()(request)
    assert response.status_code == 201


@pytest.mark.django_db
def test_genre_view_delete():
    genre = Genre.objects.create(name='Genre to be deleted')
    factory = APIRequestFactory()
    request = factory.delete('/genre/')

    response = GenreView.as_view()(request, pk=genre.name)
    # Verifique se o recurso foi excluído com sucesso
    assert response.status_code == 204


@pytest.mark.django_db
def test_genre_serializer():
    data = {'name': 'Test Serializer Genre'}
    serializer = GenreSerializer(data=data)
    # Verifique se os dados são válidos de acordo com o serializador
    assert serializer.is_valid()


@pytest.mark.django_db
def test_publisher_view_get():
    # Cria um objeto Publisher para testar a visualização
    publisher = Publisher.objects.create(name='Test Publisher')

    # Cria um mock de requisição GET
    factory = APIRequestFactory()
    request = factory.get('/publisher/')

    # Acessa a view com o método GET passando o ID do publisher
    response = PublisherView.as_view()(request, pk=publisher.id)
    assert response.status_code == 200  # Verifica se a resposta é bem-sucedida


@pytest.mark.django_db
def test_publisher_view_post():
    data = {'name': 'New Publisher'}

    factory = APIRequestFactory()
    # Define o formato como JSON
    request = factory.post('/publisher/', data, format='json')

    response = PublisherView.as_view()(request)
    assert response.status_code == 201  # Verifica se o recurso foi criado com sucesso


@pytest.mark.django_db
def test_publisher_view_delete():
    # Cria um publisher a ser excluído
    publisher = Publisher.objects.create(name='Publisher to be deleted')

    factory = APIRequestFactory()
    request = factory.delete(f'/publisher/{publisher.id}/')

    response = PublisherView.as_view()(request, pk=publisher.id)
    # Verifica se o recurso foi excluído com sucesso
    assert response.status_code == 204

# Teste para validar o funcionamento do serializador de Publisher


@pytest.mark.django_db
def test_publisher_serializer():
    data = {'name': 'Test Serializer Publisher'}
    serializer = PublisherSerializer(data=data)
    # Verifica se os dados são válidos de acordo com o serializador
    assert serializer.is_valid()
