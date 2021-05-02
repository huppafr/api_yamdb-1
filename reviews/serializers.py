from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from reviews.models import Comment, Review, Title


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):

        rq = self.context['request']
        current_title = get_object_or_404(
            Title, pk=rq.parser_context['kwargs'].get('title_id'))

        if rq.method == 'POST':
            if current_title.reviews.filter(author=rq.user).exists():
                raise serializers.ValidationError('Ваш отзыв уже оставлен')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
