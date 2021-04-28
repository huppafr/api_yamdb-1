from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField, ModelField
from django.db import models
# from rest_framework.validators import UniqueTogetherValidator

from titles.models import Category, Ganre, Title, User, Review, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GanreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Ganre


class TitleWriteSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset = Category.objects.all(),
        slug_field='name',
    )
    ganre = SlugRelatedField(
        queryset = Ganre.objects.all(),
        slug_field='name',
    )

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'ganre', 'description')
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    ganre = GanreSerializer()

    class Meta:
        fields = ('id', 'name', 'year', 'category', 'ganre', 'description')
        model = Title
