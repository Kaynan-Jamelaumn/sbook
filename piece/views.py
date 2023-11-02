from rest_framework import viewsets, generics
from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment, Page,  PieceAnotation
from .serializers import PublisherSerializer, GenreSerializer, TextContentSerializer, ImageContentSerializer, PageSerializer, ChapterSerializer, PieceSerializer, PieceAnotationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.response import Response

# class PublisherViewSet(viewsets.ModelViewSet):
#     queryset = Publisher.objects.all()
#     serializer_class = PublisherSerializer

# class GenreViewSet(viewsets.ModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff


class GenreView(APIView):
    permission_classes = [IsAdminUser]

    def to_retrieve(self, request=None, name=None):

        if name:
            genre = self.get_object(name)
        else:
            genre = self.get_object(request.data.get('name'))

        if not genre:
            return Response({"detail": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)
        return genre

    def get_object(self, name):
        try:
            return Genre.objects.get(name=name)
        except Genre.DoesNotExist:
            return None

    def get(self, request, name=None):
        if name:
            self.get_object(name)
            serializer = GenreSerializer(genre)
        else:
            genre = Genre.objects.all()
            serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_staff:
            return Response({"detail": "You do not have permission to post an Genre"}, status=status.HTTP_403_FORBIDDEN)

        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None):
        genre = self.to_retrieve(request, name)

        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        genre = self.to_retrieve(request, name)

        genre.delete()
        return Response({"detail": "Genre deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PublisherView(APIView):
    permission_classes = [IsAdminUser]

    def to_retrieve(self, request=None, id=None):
        if id:
            publisher = self.get_object(id)
        else:
            publisher = self.get_object(request.data.get('id'))

        if not publisher:
            return Response({"detail": "Publisher not found"}, status=status.HTTP_404_NOT_FOUND)
        return publisher

    def get_object(self, id):
        try:
            return Publisher.objects.get(pk=id)
        except Publisher.DoesNotExist:
            return None

    def get(self, request, id=None):
        serializer = self.to_retrieve(request, id)
        return Response(serializer.data)

    def post(self, request):

        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        publisher = self.to_retrieve(request, id)

        serializer = PublisherSerializer(
            publisher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        publisher = self.to_retrieve(request, id)
        publisher.delete()
        return Response({"detail": "Publisher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PieceList(APIView):
    def get(self, request):
        pieces = Piece.objects.all()
        serializer = PieceSerializer(pieces, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PieceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PieceDetail(APIView):
    def get_object(self, isbn):
        try:
            return Piece.objects.get(isbn=isbn)
        except Piece.DoesNotExist:
            return None

    def get(self, request, isbn):
        piece = self.get_object(isbn)
        if piece:
            serializer = PieceSerializer(piece)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, isbn):
        piece = self.get_object(isbn)
        if piece:
            serializer = PieceSerializer(piece, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, isbn):
        piece = self.get_object(isbn)
        if piece:
            piece.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ChapterList(APIView):
    def get(self, request):
        chapters = Chapter.objects.all()
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChapterDetail(APIView):
    def get_object(self, chapter_id):
        try:
            return Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return None

    def get(self, request, chapter_id):
        chapter = self.get_object(chapter_id)
        if chapter is not None:
            serializer = ChapterSerializer(chapter)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, chapter_id):
        chapter = self.get_object(chapter_id)
        if chapter is not None:
            serializer = ChapterSerializer(chapter, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, chapter_id):

        chapter = self.get_object(chapter_id)
        if chapter is not None:
            chapter.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class PageListCreateAPIView(APIView):
    def get(self, request):
        pages = Page.objects.all()
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        content_type = data.get('content_type')
        chapter_id = data.get('chapter')
        chapter_obj = Chapter.objects.get(pk=chapter_id)

        if content_type == 'text':
            text_content_serializer = TextContentSerializer(
                data=data['content']['text_content'])
            if text_content_serializer.is_valid():
                text_content = text_content_serializer.save()
                page = Page(content=text_content, chapter=chapter_obj)
                page.save()
                return Response(PageSerializer(page).data, status=status.HTTP_201_CREATED)
            return Response(text_content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif content_type == 'image':
            image_content_serializer = ImageContentSerializer(
                data=data['content']['image_content'])
            if image_content_serializer.is_valid():
                image_content = image_content_serializer.save()
                page = Page(content=image_content, chapter=chapter_obj)
                page.save()
                return Response(PageSerializer(page).data, status=status.HTTP_201_CREATED)
            return Response(image_content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid content_type'}, status=status.HTTP_400_BAD_REQUEST)


class PieceAnotationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, isbn=None):
        if isbn:
            piece = PieceAnotation.objects.filter(piece__isbn=isbn)
        else:
            piece = PieceAnotation.objects.all()
        serializer = PieceAnotationSerializer(piece, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        isbn = request.data.get('isbn')
        piece = Piece.objects.get(isbn=isbn)
        serializer = PieceAnotationSerializer(data=request.data)
        if serializer.is_valid() and piece:
            serializer.save(user=request.user, piece=piece)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        piece_anotation_id = request.data.get('anotation')
        piece_anotation = PieceAnotation.objects.get(id=piece_anotation_id)
        if request.user == piece_anotation.user or request.user.is_staff:
            piece_anotation.delete()
            return Response({"detail": "Piece deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to delete this piece"}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        piece_anotation_id = request.data.get('anotation')
        piece_anotation = PieceAnotation.objects.get(id=piece_anotation_id)
        if piece_anotation and (request.user == piece_anotation.user or request.user.is_staff):
            serializer = PieceAnotationSerializer(
                piece_anotation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
