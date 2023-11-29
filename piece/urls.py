from django.urls import path
from .views import (
    GenreView,
    PublisherView,
    PieceView,
    SearchFilterView,
    ChapterView,
    PageView,
    PieceAnotationView,
    PieceAnotationContentView,
    PieceAnotationByUserView,
    PieceAnotationContentAndUserView,
    PieceStatusView,
    StatusByPieceView,
    StatusByUserView,
    PieceRatingAverageView


)

urlpatterns = [
    path('genre/<str:pk>/', GenreView.as_view(), name='genre-detail'),
    path('genre/', GenreView.as_view(), name='genre'),

    path('publisher/', PublisherView.as_view(), name='publisher'),
    path('publisher/<str:pk>/', PublisherView.as_view(), name='publisher-detail'),

    path('piece/', PieceView.as_view(), name='piece-list'),
    path('piece/<str:pk>/', PieceView.as_view(), name='piece-detail'),
    path('search/', SearchFilterView.as_view(), name='search'),

    path('chapter/', ChapterView.as_view(), name='chapter-list'),
    path('chapter/<str:pk>/', ChapterView.as_view(), name='chapter-detail'),

    path('page/', PageView.as_view(), name='page-list'),

    path('status/', PieceStatusView.as_view(), name='piece-status-list'),
    path('status/<str:pk>/', PieceStatusView.as_view(),
         name='piece-status-detail'),
    path('status/piece/', StatusByPieceView.as_view(),
         name='piece-status-by-piece-list'),
    path('status/piece/<str:piece>/', StatusByPieceView.as_view(),
         name='piece-status-by-piece-list'),
    path('status/user/', StatusByUserView.as_view(),
         name='piece-status-by-user-list'),
    path('status/user/<str:user>/', StatusByUserView.as_view(),
         name='piece-status-by-user-list'),


    path('anotation/', PieceAnotationView.as_view(), name='piece-anotation-list'),
    path('anotation/<str:pk>/', PieceAnotationView.as_view(),
         name='piece-anotation-detail'),
    path('anotation/content/', PieceAnotationContentView.as_view(),
         name='piece-anotation-content-list'),
    path('anotation/user/', PieceAnotationByUserView.as_view(),
         name='piece-anotation-by-user-list'),
    path('anotation/user/<str:user>/', PieceAnotationByUserView.as_view(),
         name='piece-anotation-by-user-list'),
    path('anotation/content-and-user/', PieceAnotationContentAndUserView.as_view(),
         name='piece-anotation-content-and-user-list'),

    path('piece/<str:pk>/average-rating/',
         PieceRatingAverageView.as_view(), name='piece-average-rating'),
]
