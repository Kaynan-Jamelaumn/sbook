from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreList,
    GenreDetail,
    PublisherList,
    PublisherDetail,

    PieceList,
    PieceDetail,

    ChapterList,
    ChapterDetail,

    PageListCreateAPIView,

    PieceAnotationAPIView
)


urlpatterns = [
    path('genre/<str:name>/', GenreDetail.as_view(), name='genre-detail'),
     path('genre/', GenreList.as_view(), name='genre'),
    path('publisher/', PublisherList.as_view(), name='publisher'),
    path('publisher/<int:id>/',
         PublisherDetail.as_view(), name='publisher-detail'),
    path('pieces/', PieceList.as_view(), name='piece-list'),
    path('pieces/<str:isbn>/', PieceDetail.as_view(), name='piece-detail'),
    path('chapter/', ChapterList.as_view(), name='chapter-list'),
    path('chapter/<int:chapter_id>/', ChapterDetail.as_view(), name='chapter-detail'),
    path('pages/', PageListCreateAPIView.as_view(), name='page-list-create'),
    path('anotation/', PieceAnotationAPIView.as_view(), name='piece-anotation'),
    path('anotation/<str:isbn>/', PieceAnotationAPIView.as_view(), name='pxiece-anotation'),
]