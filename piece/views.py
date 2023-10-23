from rest_framework import viewsets
from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment
from .serializers import PublisherSerializer, GenreSerializer, PieceSerializer, ChapterSerializer, PageContentSerializer, TextContentSerializer, ImageContentSerializer, CommentSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TextContentViewSet(viewsets.ModelViewSet):
    queryset = TextContent.objects.all()
    serializer_class = TextContentSerializer

class ImageContentViewSet(viewsets.ModelViewSet):
    queryset = ImageContent.objects.all()
    serializer_class = ImageContentSerializer

class PageContentViewSet(viewsets.ModelViewSet):
    queryset = PageContent.objects.all()
    serializer_class = PageContentSerializer

class PieceViewSet(viewsets.ModelViewSet):
    queryset = Piece.objects.all()
    serializer_class = PieceSerializer

class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer