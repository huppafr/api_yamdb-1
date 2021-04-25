from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from django.http import HttpResponse, Http404
from .models import Title, Comment, Review
from .api.serializers import ReviewsSerializer, CommentsSerializer
from .api.permissions import IsAuthor
User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewsSerializer
    permission_classes = [
        IsAuthor,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs['title_id']))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return HttpResponse(status=404)
        return HttpResponse(status=204)


class CommentsViewSet(viewsets.ModelViewSet):

    serializer_class = CommentsSerializer
    permission_classes = [
        IsAuthor,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, pk=self.kwargs['review_id']))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            return HttpResponse(status=404)
        return HttpResponse(status=204)
