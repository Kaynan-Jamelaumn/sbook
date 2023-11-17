from rest_framework import serializers
from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment, Page,  PieceAnotation, PieceStatus
from main.serializers import AuthorSerializer, CustomUserSerializer


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PieceSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = AuthorSerializer(
            instance.author, many=True).data

        representation['user'] = CustomUserSerializer(
            instance.user, many=True).data

        representation['genre'] = GenreSerializer(
            instance.genre, many=True).data
        return representation

    class Meta:
        model = Piece
        fields = '__all__'

    def validate(self, data):
        if not data.get('author') and not data.get('user'):
            raise serializers.ValidationError(
                "Either an author or a user must be provided.")

        return data


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class TextContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextContent
        fields = '__all__'


class ImageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageContent
        fields = '__all__'


class PageContentSerializer(serializers.Serializer):
    text_content = TextContentSerializer(required=False)
    image_content = ImageContentSerializer(required=False)


class PageSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if isinstance(obj.content, TextContent):
            serializer = TextContentSerializer(obj.content)
        elif isinstance(obj.content, ImageContent):
            serializer = ImageContentSerializer(obj.content)
        else:
            serializer = PageContentSerializer(obj.content)
        return serializer.data

    class Meta:
        model = Page
        fields = '__all__'


class PieceAnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceAnotation
        fields = '__all__'


class PieceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceStatus
        fields = '__all__'
