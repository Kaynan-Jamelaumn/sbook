from django.urls import path
from .views import (
    GenreView,
    PublisherView,
    PieceView,
    SearchFilterView,
    ChapterView,
    PageView,
    PieceAnotationView,
    PieceStatusView
)


urlpatterns = [
    path('genre/<str:pk>/', GenreView.as_view(), name='genre-detail'),
    path('genre/', GenreView.as_view(), name='genre'),
    path('publisher/', PublisherView.as_view(), name='publisher'),
    path('publisher/<str:pk>/',
         PublisherView.as_view(), name='publisher-detail'),
    path('piece/', PieceView.as_view(), name='piece-list'),
    path('piece/<str:pk>/', PieceView.as_view(), name='piece-detail'),
    path('search/',
         SearchFilterView.as_view(), name='search'),
    path('chapter/', ChapterView.as_view(), name='chapter'),
    path('chapter/<str:pk>/',
         ChapterView.as_view(), name='chapter-detail'),
    path('page/', PageView.as_view(), name='page'),
    path('anotation/', PieceAnotationView.as_view(), name='piece-anotation'),
    path('anotation/<str:pk>/', PieceAnotationView.as_view(),
         name='peiece-anotation'),
    path('status/', PieceStatusView.as_view(), name='piece-status'),
    path('status/<str:pk>/', PieceStatusView.as_view(),
         name='piece-status'),
]
