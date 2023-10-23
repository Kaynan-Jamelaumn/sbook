from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PublisherViewSet, GenreViewSet, TextContentViewSet, ImageContentViewSet, PageContentViewSet, PieceViewSet, ChapterViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'publishers', PublisherViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'textcontents', TextContentViewSet)
router.register(r'imagecontents', ImageContentViewSet)
router.register(r'pagecontents', PageContentViewSet)
router.register(r'pieces', PieceViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'comments', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
