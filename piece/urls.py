from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreView,
    PublisherView,
    PieceList,
    PieceDetail,

    ChapterList,
    ChapterDetail,

    PageListCreateAPIView,

    PieceAnotationAPIView
)


urlpatterns = [
    path('genre/<str:name>/', GenreView.as_view(), name='genre-detail'),
    path('genre/', GenreView.as_view(), name='genre'),
    path('publisher/', PublisherView.as_view(), name='publisher'),
    path('publisher/<int:id>/',
         PublisherView.as_view(), name='publisher-detail'),
    path('pieces/', PieceList.as_view(), name='piece-list'),
    path('pieces/<str:isbn>/', PieceDetail.as_view(), name='piece-detail'),
    path('chapter/', ChapterList.as_view(), name='chapter-list'),
    path('chapter/<int:chapter_id>/',
         ChapterDetail.as_view(), name='chapter-detail'),
    path('pages/', PageListCreateAPIView.as_view(), name='page-list-create'),
    path('anotation/', PieceAnotationAPIView.as_view(), name='piece-anotation'),
    path('anotation/<str:isbn>/', PieceAnotationAPIView.as_view(),
         name='pxiece-anotation'),
]
