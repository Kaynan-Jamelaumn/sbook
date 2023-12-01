from rest_framework import serializers
from .models import Publisher, Genre,  Piece, Chapter, PageContent, TextContent, ImageContent, Comment, Page,  PieceAnotation, PieceStatus
from main.serializers import AuthorSerializer, CustomUserSerializer

from decimal import Decimal, ROUND_HALF_UP


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PieceSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, instance):
        try:
            ratings = PieceStatus.objects.filter(piece=instance, rating__isnull=False).values_list('rating', flat=True)

            average_rating = sum(ratings) / len(ratings)
            # Arredonde a média para .0 ou .5
            rounded_rating = Decimal(average_rating).quantize(
                Decimal('0.0'), rounding=ROUND_HALF_UP)
            return float(rounded_rating)
        except ZeroDivisionError:
            return 0

    def validate(self, data):
        if self.instance is None:

            if not data.get('authors') and not data.get('users'):
                raise serializers.ValidationError(
                    "Either an author or a user must be provided.")

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['authors'] = AuthorSerializer(
            instance.authors, many=True).data

        representation['users'] = CustomUserSerializer(
            instance.users, many=True).data

        representation['genres'] = GenreSerializer(
            instance.genres, many=True).data

        representation['publisher'] = PublisherSerializer(
            instance.publisher).data
        return representation

    class Meta:
        model = Piece
        fields = '__all__'


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(
            instance.user).data

        representation['piece'] = PieceSerializer(
            instance.piece).data
        return representation

    class Meta:
        model = PieceAnotation
        fields = '__all__'


class PieceStatusSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = CustomUserSerializer(
            instance.user).data

        representation['piece'] = PieceSerializer(
            instance.piece).data
        return representation

    class Meta:
        model = PieceStatus
        fields = '__all__'
