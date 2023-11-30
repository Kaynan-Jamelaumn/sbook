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
    StatusByUserFilteringByStatusChoieceView,
)

urlpatterns = [
    path('genre/<str:pk>/', GenreView.as_view(), name='genre-detail'),
    path('genre/', GenreView.as_view(), name='genre'),

    path('publisher/', PublisherView.as_view(), name='publisher-list'),
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
         name='piece-status-by-piece-detail'),
    path('status/user/', StatusByUserView.as_view(),
         name='piece-status-by-user-list'),
    path('status/user/<str:user>/', StatusByUserView.as_view(),
         name='piece-status-by-user-detail'),

    path('status/search/user/', StatusByUserFilteringByStatusChoiceView.as_view(),
         name='piece-status-search-by-user'),
    path('status/search/user/<str:user>/', StatusByUserFilteringByStatusChoiceView.as_view(),
         name='piece-status-search-by-user-detail'),

    path('anotation/', PieceAnotationView.as_view(),
         name='piece-annotation-list'),
    path('anotation/<str:pk>/', PieceAnotationView.as_view(),
         name='piece-annotation-detail'),
    path('anotation/content/', PieceAnotationContentView.as_view(),
         name='piece-annotation-content-list'),
    path('anotation/user/', PieceAnotationByUserView.as_view(),
         name='piece-annotation-by-user-list'),
    path('anotation/user/<str:user>/', PieceAnotationByUserView.as_view(),
         name='piece-annotation-by-user-detail'),
    path('anotation/content-and-user/', PieceAnotationContentAndUserView.as_view(),
         name='piece-annotation-content-and-user-list'),
]
