from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Review, Comment, Title, Ganre
from django.db.models import Avg

User = get_user_model()


class ReviewsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentsSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ganre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Ganre


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(read_only=True, many=True)
    category = GenreSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = (
            'id', 'rating', 'name', 'year', 'author', 'genre', 'category')
        model = Title

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj.id).aggregate(Avg('score'))
        return rating['score__avg']
