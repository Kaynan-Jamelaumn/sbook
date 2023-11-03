from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment, Page,  PieceAnotation
from .serializers import PublisherSerializer, GenreSerializer, TextContentSerializer, ImageContentSerializer, PageSerializer, ChapterSerializer, PieceSerializer, PieceAnotationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.response import Response


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff


class GenreView(APIView):
    def is_allowed(self, request):
        if not request.user.is_staff:
            return Response({"detail": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

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
        if name or request.data.get('name'):
            self.to_retrieve(request, name)
            serializer = GenreSerializer(genre)
        else:
            genre = Genre.objects.all()
            serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.is_allowed(self, request)
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, name=None):
        self.is_allowed(self, request)
        genre = self.to_retrieve(request, name)

        serializer = GenreSerializer(genre, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name=None):
        self.is_allowed(self, request)
        genre = self.to_retrieve(request, name)

        genre.delete()
        return Response({"detail": "Genre deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PublisherView(APIView):
    def is_allowed(self, request):
        if not request.user.is_staff:
            return Response({"detail": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

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
        if id or request.data.get('id'):
            publisher = self.to_retrieve(request, id)
            serializer = PublisherSerializer(publisher)
        else:
            publisher = Publisher.objects.all()
            serializer = PublisherSerializer(publisher, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request):
        self.is_allowed(self, request)
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        self.is_allowed(self, request)
        publisher = self.to_retrieve(request, id)

        serializer = PublisherSerializer(
            publisher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        self.is_allowed(self, request)
        publisher = self.to_retrieve(request, id)
        publisher.delete()
        return Response({"detail": "Publisher deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class PieceView(APIView):

    def to_retrieve(self, request=None, isbn=None):
        if isbn:
            piece = self.get_object(isbn)
        else:
            piece = self.get_object(request.data.get('isbn'))

        if not piece:
            return Response({"detail": "Piece not found"}, status=status.HTTP_404_NOT_FOUND)
        return piece

    def get_object(self, isbn):
        try:
            return Piece.objects.get(isbn=isbn)
        except Piece.DoesNotExist:
            return None

    def get(self, request, isbn=None):
        if isbn or request.data.get('isbn'):
            piece = self.to_retrieve(request, isbn)
            serializer = PieceSerializer(piece)
        else:
            piece = Piece.objects.all()
            serializer = PieceSerializer(piece, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PieceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, isbn=None):
        piece = self.to_retrieve(request, isbn)
        serializer = PieceSerializer(piece, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, isbn=None):
        piece = self.to_retrieve(request, isbn)
        piece.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChapterView(APIView):
    def to_retrieve(self, request=None, id=None):
        if id:
            piece = self.get_object(id)
        else:
            piece = self.get_object(request.data.get('id'))

        if not piece:
            return Response({"detail": "Piece not found"}, status=status.HTTP_404_NOT_FOUND)
        return piece

    def get_object(self, id):
        try:
            return Chapter.objects.get(id=id)
        except Chapter.DoesNotExist:
            return None

    def get(self, request, id=None):
        if id or request.data.get('id'):
            chapter = self.to_retrieve(request, id)
            serializer = ChapterSerializer(chapter)
        else:
            chapter = Chapter.objects.all()
            serializer = ChapterSerializer(chapter, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ChapterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, chapter_id):
        chapter = self.get_object(chapter_id)
        serializer = ChapterSerializer(
            chapter, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, chapter_id):

        chapter = self.to_retrieve(request, chapter_id)
        chapter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PageView(APIView):
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


class PieceAnotationView(APIView):
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
