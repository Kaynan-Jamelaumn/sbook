from django.urls import path
from .views import (
    GenreView,
    PublisherView,
    PieceView,
    ChapterView,
    PageView,
    PieceAnotationView
)


urlpatterns = [
    path('genre/<str:name>/', GenreView.as_view(), name='genre-detail'),
    path('genre/', GenreView.as_view(), name='genre'),
    path('publisher/', PublisherView.as_view(), name='publisher'),
    path('publisher/<int:id>/',
         PublisherView.as_view(), name='publisher-detail'),
    path('pieces/', PieceView.as_view(), name='piece-list'),
    path('pieces/<str:isbn>/', PieceView.as_view(), name='piece-detail'),
    path('chapter/', ChapterView.as_view(), name='chapter-list'),
    path('chapter/<int:chapter_id>/',
         ChapterView.as_view(), name='chapter-detail'),
    path('pages/', PageView.as_view(), name='page-list-create'),
    path('anotation/', PieceAnotationView.as_view(), name='piece-anotation'),
    path('anotation/<str:isbn>/', PieceAnotationView.as_view(),
         name='pxiece-anotation'),
]
