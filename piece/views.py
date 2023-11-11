from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment, Page,  PieceAnotation, PieceStatus
from .serializers import PublisherSerializer, GenreSerializer, TextContentSerializer, ImageContentSerializer, PageSerializer, ChapterSerializer, PieceSerializer, PieceStatusSerializer, PieceAnotationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, BasePermission
from rest_framework.response import Response


# class IsAdminOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return True
#         return request.user and request.user.is_staff


class BaseView(APIView):

    def __init__(self, model, param_name, serializer):
        self.__model = model
        self.__param_name = param_name
        self.__serializer = serializer

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        self.__model = value

    @property
    def param_name(self):
        return self.__param_name

    @param_name.setter
    def param_name(self, value):
        self.__param_name = value

    @property
    def serializer(self):
        return self.__serializer

    @serializer.setter
    def serializer(self, value):
        self.__serializer = value

    def is_allowed(self, request, permission_type=None):
        if not request.user.is_staff:
            if permission_type:
                return Response({f"error": "You do not have the necessary permission to {permission_type} an/a {self.model}"}, status=status.HTTP_403_FORBIDDEN)
            return Response({"error": "You do not have the necessary permissions"}, status=status.HTTP_403_FORBIDDEN)

    def check_obj(self, obj):
        if not obj:
            return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

    def to_retrieve(self, request=None, pk=None, many=False):

        if pk:
            if many == True:
                obj = self.get_object(pk=pk, many=True)
                self.check_obj(obj)
                serializer = self.serializer(obj,  many=True)
            else:
                obj = self.get_object(pk)
                self.check_obj(obj)
                serializer = self.serializer(obj)
        elif request.data.get(self.param_name):
            if many == True:
                obj = self.get_object(request, many=True)
                self.check_obj(obj)
                serializer = self.__serializer(obj, many=True)
            else:
                obj = self.get_object(request)
                self.check_obj(obj)
                serializer = self.__serializer(obj)

        else:
            serializer = self.__serializer(
                data=self.model.objects.all(), many=True)
            serializer.is_valid()
        return serializer

    def get_object(self, pk, request=None, many=False):
        if many == True:
            if pk:
                # Retorna o primeiro objeto correspondente.__param_name: pk})
                obj = self.model.objects.filter(**{self.__param_name: pk})
            else:
                obj = self.model.objects.filter(
                    **{self.__param_name: request.data.get(self.__param_name)})
        else:
            if pk:
                # Retorna o primeiro objeto correspondente.__param_name: pk})
                obj = self.model.objects.get(**{self.__param_name: pk})
            else:
                obj = self.model.objects.get(
                    **{self.__param_name: request.data.get(self.__param_name)})
        if obj:
            return obj
        return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk=None):
        serializer = self.to_retrieve(request, pk)
        return Response(serializer.data,  status=status.HTTP_200_OK)

    def post(self, request, allowed=False):
        if not allowed:
            self.is_allowed(request)
        elif request.user.is_authenticated:
            return Response({"error": f"You must be logged in to post a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, allowed=False):
        if not allowed:
            self.is_allowed(request)
        elif request.user.is_authenticated:
            return Response({"error": f"You must be logged in to edit a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        obj = self.get_object(pk, request)
        print("teste", obj)
        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, allowed=False):
        if not allowed:
            self.is_allowed(request)
        elif request.user.is_authenticated:
            return Response({"error": f"You must be logged in to delete a/an{self.model.__name__}"}, status=status.HTTP_403_FORBIDDEN)
        obj = self.get_object(pk, request)
        obj.delete()
        return Response({"detail": f"{self.model.__name__} deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class GenreView(BaseView):
    def __init__(self, model=Genre, param_name="name", serializer=GenreSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request)

    def put(self, request):
        return Response({"error": f"Not Allowed"}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk=None):
        return super().delete(request, pk)


class PublisherView(BaseView):
    def __init__(self, model=Publisher, param_name="id", serializer=PublisherSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request)

    def put(self, request, pk=None):
        return super().put(request, pk)

    def delete(self, request, pk=None):
        return super().delete(request, pk)


class PieceView(BaseView):
    def __init__(self, model=Piece, param_name="isbn", serializer=PieceSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request, True)

    def put(self, request, pk=None):
        return super().put(request, pk, True)

    def delete(self, request, pk=None):
        return super().delete(request, True)


class SearchFilterView(APIView):

    def get(self, request, pk=None):
        objects = []


class ChapterView(BaseView):
    def __init__(self, model=Chapter, param_name="id", serializer=ChapterSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request, True)

    def put(self, request, pk=None):
        return super().put(request, pk, True)

    def delete(self, request, pk=None):
        return super().delete(request, True)


class PageView(BaseView):
    def __init__(self, model=Page, param_name="id", serializer=PageSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

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

    def put(self, request, pk=None):
        page_obj = self.get_object(pk, request)

        if not page_obj:
            return Response({"error": f"{self.model.__name__} not found"}, status=status.HTTP_404_NOT_FOUND)

        # Determine the content type from the request data
        content_type = request.data.get('content_type')

        # Handle the update according to the content type
        if content_type == 'text':
            text_content_serializer = TextContentSerializer(
                page_obj.content, data=request.data['content']['text_content'], partial=True)
            if text_content_serializer.is_valid():
                text_content_serializer.save()
                return Response(PageSerializer(page_obj).data, status=status.HTTP_200_OK)
            return Response(text_content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif content_type == 'image':
            image_content_serializer = ImageContentSerializer(
                page_obj.content, data=request.data['content']['image_content'], partial=True)
            if image_content_serializer.is_valid():
                image_content_serializer.save()
                return Response(PageSerializer(page_obj).data, status=status.HTTP_200_OK)
            return Response(image_content_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'Invalid content_type'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        return super().delete(request, True)


class PieceStatusView(BaseView):
    def __init__(self, model=PieceStatus, param_name="id", serializer=PieceStatusSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request, True)

    def put(self, request, pk=None):
        return super().put(request, pk, True)

    def delete(self, request, pk=None):
        return super().delete(request, True)


class PieceAnotationView(BaseView):
    def __init__(self, model=PieceAnotation, param_name="id", serializer=PieceAnotationSerializer):
        super().__init__(model, param_name, serializer)

    def get(self, request, pk=None):
        return super().get(request, pk)

    def post(self, request):
        return super().post(request, True)

    def put(self, request, pk=None):
        return super().put(request, pk, True)

    def delete(self, request, pk=None):
        return super().delete(request, True)
